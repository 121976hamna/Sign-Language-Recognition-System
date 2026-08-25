import serial
import csv
import time
import os

# Set your port and baud rate
arduino = serial.Serial('COM4', 9600)  # Change COM port as needed
filename = 'urdu_gesture_data.csv'

# Load existing data to prevent duplicates
existing_data = set()

if os.path.exists(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            existing_data.add(tuple(map(int, row[:5])))

print("Starting gesture data collection...")

# Open file for appending new data
with open(filename, 'a', newline='') as file:
    writer = csv.writer(file)
    if os.stat(filename).st_size == 0:
        writer.writerow(['f1', 'f2', 'f3', 'f4', 'f5', 'label'])

    try:
        while True:
            print("\nShow a new gesture. Recording for 5 seconds...")
            buffer = []
            start_time = time.time()

            while time.time() - start_time < 5:
                if arduino.in_waiting:
                    line = arduino.readline().decode().strip()
                    if line:
                        try:
                            data = tuple(map(int, line.split(',')))
                            if len(data) == 5 and data not in existing_data:
                                buffer.append(data)
                        except:
                            continue

            if buffer:
                label = input(f"\nCaptured {len(buffer)} unique values. Enter alphabet name (or press Enter to skip): ")
                if label:
                    for row in buffer:
                        writer.writerow(list(row) + [label])
                        existing_data.add(row)
                    print(f"✅ {len(buffer)} rows saved under label: {label}")
                else:
                    print("⛔ Skipped saving this batch.")
            else:
                print("⚠️ No new unique gesture data captured. Try again.")
    except KeyboardInterrupt:
        print("\n🛑 Data collection stopped.")
