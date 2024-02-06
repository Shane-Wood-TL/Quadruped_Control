#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>



const int bufferSize = 64; // Adjust the buffer size based on your needs
char buffer[bufferSize];
int index = 0;


String oldPrint;
String receivedStringG;

int splitAndConvert(String input, float* values, int maxValues);



void setup() {

  Serial.begin(9600);
  while (!Serial) {
    // Wait for the serial port to initialize
  }
}
void loop() {
  // Check if data is available to read
  while (Serial.available() > 0) {
    char incomingChar = Serial.read(); // Read a character from the serial buffer

    // Check if the received character is a newline character
    if (incomingChar == '\n') {
      // Null-terminate the buffer to make it a valid C-string
      buffer[index] = '\0';

      // Process the received string
      String receivedString(buffer);
      receivedStringG = receivedString;
      //Serial.print("Received string: ");
      //Serial.println(receivedString);

      // Reset the buffer index for the next string
      index = 0;
    } else {
      // If the character is not a newline, add it to the buffer
      if (index < bufferSize - 1) {
        buffer[index] = incomingChar;
        index++;
      }
    }
  }
  if (receivedStringG != oldPrint){
    Serial.println(receivedStringG);
    oldPrint = receivedStringG;
  }


  const int maxValues = 10; // Set the maximum number of values you expect
  float values[maxValues];  // Array to store the floating-point values

  // Split the string by commas and convert to floats
  int count = splitAndConvert(oldPrint, values, maxValues);

  // Print the results
  for (int i = 0; i < count; i++) {
    Serial.print("Float ");
    Serial.print(i + 1);
    Serial.print(": ");
    Serial.println(values[i]);
  }
}


int splitAndConvert(String input, float* values, int maxValues) {
  int count = 0;
  int lastIndex = 0;
  int currentIndex = input.indexOf(',');

  while (currentIndex != -1 && count < maxValues) {
    String substring = input.substring(lastIndex, currentIndex);
    values[count] = atof(substring.c_str());

    lastIndex = currentIndex + 1;
    currentIndex = input.indexOf(',', lastIndex);
    count++;
  }

  // Process the last value after the last comma
  String lastSubstring = input.substring(lastIndex);
  values[count] = atof(lastSubstring.c_str());
  count++;

  return count;
}