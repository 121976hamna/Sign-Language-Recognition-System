/*
void setup() {
  Serial.begin(9600);
  }

void loop() {
  int f1 = analogRead(A0);
  int f2 = analogRead(A1);
  int f3 = analogRead(A2);
  int f4 = analogRead(A3);
  int f5 = analogRead(A4);

  Serial.print(f1); Serial.print(",");
  Serial.print(f2); Serial.print(",");
  Serial.print(f3); Serial.print(",");
  Serial.print(f4); Serial.print(",");
  Serial.println(f5);

  delay(100);  // Adjust delay for smoother predictions
 }

*/
#include "SoftwareSerial.h"
#include "DFRobotDFPlayerMini.h"

static const uint8_t PIN_MP3_TX = 2;  // Connects to DFPlayer RX
static const uint8_t PIN_MP3_RX = 3;  // Connects to DFPlayer TX
SoftwareSerial softwareSerial(PIN_MP3_RX, PIN_MP3_TX);

DFRobotDFPlayerMini player;

const int flexPins[5] = { A0, A1, A2, A3, A4 };  // Flex sensor pins for left hand

void setup() {
  Serial.begin(9600);          // Communication with Python
  softwareSerial.begin(9600);  // Communication with DFPlayer

  if (player.begin(softwareSerial)) {
    Serial.println("DFPlayer Ready");
    player.volume(30);  // Set volume from 0 to 30
  } else {
    Serial.println("Connecting to DFPlayer Mini failed!");
  }
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "Global") {
      player.play(7);  // 0007.mp3
    } else if (command == "Alif") {
      player.play(1);
    } else if (command == "Jeem") {
      player.play(2);
    } else if (command == "Chay") {
      player.play(3);
    } else if (command == "Zoay") {
      player.play(4);
    } else if (command == "Fay") {
      player.play(5);
    }  else if (command == "Laam") {
      player.play(6);
    } else if (command == "GetData") {
      // Read and send flex sensor values
      String data = "";
      for (int i = 0; i < 5; i++) {
        data += String(analogRead(flexPins[i]));
        if (i < 4) data += ",";  // For separating with commas
      }
      Serial.println(data);
    }
  }
}

