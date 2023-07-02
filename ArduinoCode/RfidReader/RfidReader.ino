#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9

MFRC522 rfid(SS_PIN, RST_PIN); // Create an instance of MFRC522

void setup() {
  Serial.begin(9600); // Initialize serial communication at a baud rate of 9600
  pinMode(LED_BUILTIN, OUTPUT); // Set the LED_BUILTIN pin as an output
  SPI.begin(); // Initialize the SPI bus
  rfid.PCD_Init(); // Initialize the RC522 module
}

void loop() {
  if (rfid.PICC_IsNewCardPresent()) {
    // If a new card is detected
    if (rfid.PICC_ReadCardSerial()) {
      // If the serial number (UID) of the card is successfully read
      for (byte i = 0; i < rfid.uid.size; i++) {
        Serial.print(rfid.uid.uidByte[i] < 0x10 ? "0" : ""); // Print the UID byte in hexadecimal format
        Serial.print(rfid.uid.uidByte[i], HEX);
      }
      Serial.println(); // Print a new line
      digitalWrite(LED_BUILTIN, HIGH); // Turn on the built-in LED
      delay(1000); // Delay for 1 second
      digitalWrite(LED_BUILTIN, LOW); // Turn off the built-in LED
      rfid.PICC_HaltA(); // Deactivate the card
    }
  }
}