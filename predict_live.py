import serial
import joblib
import time

# Load trained model
model = joblib.load('urdu_sign_model.pkl')

# Connect to Arduino (update COM port if needed)
arduino = serial.Serial('COM4', 9600)
time.sleep(2)

# All valid Urdu alphabet gestures
valid_gestures = {
    'Alif', 'Jeem', 'Chay', 'Zoay', 'Fay', 'Laam'
}

print("🔄 Urdu Flex Gesture System Started")

# Play Global Message ONCE at start
arduino.write(b"Global\n")
print("🔊 Playing: Perform a gesture for an alphabet")
time.sleep(10)  # Wait for Global message to finish

previous_prediction = None

# Threshold to detect if hand is at rest
rest_threshold = 20  # You can adjust this
last_values = [0, 0, 0, 0, 0]

# Smoothing settings
smooth_readings = []
smooth_window_size = 3  # How many readings to average

# Reminder settings 
reminder_interval = 10  # seconds
last_gesture_time = time.time()  # Initialize with current time

def is_hand_rest(current_values, last_values, threshold):
    differences = [abs(c - l) for c, l in zip(current_values, last_values)]
    return all(diff < threshold for diff in differences)

def average_readings(readings):
    # Take column-wise average
    averaged = []
    for i in range(5):  # 5 sensors
        col = [reading[i] for reading in readings]
        averaged.append(sum(col) // len(col))
    return averaged

try:
    while True:
        # Step 1: Global Prompt
        arduino.write(b"Global\n")
        print("🔊 Playing: Perform a gesture for an alphabet")
        time.sleep(5)  # Wait for Global message to finish

        gesture_confirmed = False

        while not gesture_confirmed:
            # Step 2: Wait for valid gesture
            arduino.write(b"GetData\n")
            time.sleep(0.3)

            if arduino.in_waiting:
                raw = arduino.readline().decode().strip()
                print("📥 Raw Serial:", raw)

                if any(skip in raw for skip in ["DFPlayer Ready", "Connecting"]):
                    continue

                try:
                    values = list(map(int, raw.split(',')))
                    print("📦 Sensor Values:", values)

                    if len(values) == 5:
                        if is_hand_rest(values, last_values, rest_threshold):
                            print("🛌 Hand at Rest - No prediction")
                            smooth_readings.clear()
                            continue

                        smooth_readings.append(values)
                        if len(smooth_readings) > smooth_window_size:
                            smooth_readings.pop(0)

                        if len(smooth_readings) == smooth_window_size:
                            averaged_values = average_readings(smooth_readings)
                            print("📊 Averaged Sensor Values:", averaged_values)
                            prediction = model.predict([averaged_values])[0]
                            print(f"🖐 Predicted: {prediction}")

                            if prediction in valid_gestures and prediction != previous_prediction:
                                arduino.write((prediction + "\n").encode())
                                print(f"🔊 Playing: {prediction}")
                                previous_prediction = prediction
                                time.sleep(1)  # Give Arduino time to play the sound

                                # Step 3: Ask for user confirmation
                                response = input("✅ Is your gesture correct? (Y/N): ").strip().upper()
                                if response == "Y":
                                    print("⏳ Waiting 10 seconds before next round...")
                                    time.sleep(10)
                                    gesture_confirmed = True  # Move to next round
                                else:
                                    print("🔁 Let's try again...")
                                    smooth_readings.clear()                                
                                    last_values = [0, 0, 0, 0, 0]
                                    break  # Replay Global message

                            last_values = averaged_values

                except Exception as e:
                    print("⚠️ Error:", e)

except KeyboardInterrupt:
    print("\n🛑 Program exited.")
    arduino.close()