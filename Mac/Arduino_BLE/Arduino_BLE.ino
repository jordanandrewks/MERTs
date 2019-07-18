// Jordan Andrew 'sloth' Small VERSION 2!!!!!
// MEng Final Year Project 2018 - 2019
// Arduino File: BLE2
// Description:  Connects to computer through Bluetooth, the pyhton script on the MASTER computer
// - sends a BPM values which appear on the output of the piezo bender.

#include "SoftwareSerial.h"
SoftwareSerial serial_connection(10, 11);  // Serial connection through pins 10 & 11
#define BUFFER_SIZE 256                    // Create buffer size (capture data)
char inData[BUFFER_SIZE];                  // Data recieved - sizeof Buffer
char inChar = -1;                           // Initialie the first character as nothing
int count = 0;                              //This is the number of lines sent in from the python script
int i = 0;                                  //Arduinos are not the most capable chips in the world so I just create the looping variable once
int j = 0;
int k = 0;
float bpmValue = 0;  // For demonstration only
float bpm_val_per_min_toSeconds;
int jnd_count = 0;
bool pulse_state;

bool JND_testing;

bool const_first; // If 0 then the consant must go first

bool const_second;

int constant_test;

int temp_test;

int stage_one = 0;
int stage_two = 0;
int jnd_counter = 0;

bool bts_perception;

void setup() {
  Serial.begin(9600);             //Initialize communications to the serial monitor in the Arduino IDE
  serial_connection.begin(9600);  //Initialize communications with the bluetooth module
  serial_connection.println("Connection Start");  //Send something to just start comms. This will never be seen.
  Serial.println("Started");  //Tell the serial monitor that the sketch has started.

  // Setting the digital output pins 0 - 7
  for (int i = 0; i < 8; i++) {
    pinMode(i, OUTPUT);
  }
}



void loop() {
  byte byte_count = serial_connection.available();  // This gets the number of bytes that were sent by the python script

  char headerData[3];

  if (byte_count) {                     // Here is activated if the user from python
    Serial.print("Ready to recieve");

    Serial.println("\nIncoming Data");      // Signal to the monitor that something is happening
    int first_bytes = byte_count;           // initialize the number of bytes that we might handle.
    int remaining_bytes = 0;                // Initialize the bytes that we may have to burn off to prevent a bufferoverrun
    Serial.print("Bytes ");
    Serial.println(first_bytes);


    // Get Window Size of the incoming  | Window size ensures all data is gathered
    int window_extraction = serial_connection.read();

    char window_char[BUFFER_SIZE];          // Buffer Size set to 64 bytes as standard

    window_char[0] = window_extraction;     // The window size is extracted from the first bit of the header

    window_char[1] = '\0';                  // End it with a null terminatior

    Serial.println(window_char[0]);         // Print the window size String format

    int window_size = atoi(window_char);    // Convert into a Integer to state how big the window size is

    Serial.println(window_size);            // Print the window size in Int format


    // Extract Message  | Store within inData
    for (i = 1; i <= window_size; i++) {    // Start from 1 then Handle each byte
      inChar = serial_connection.read();    // Read one byte
      inData[i] = inChar;                   // Put it into a character string (Array)
      Serial.println(String(inChar));
    }

    inData[i] = '\0';       //  End with null terminator.


    //  EXTRACT HEADER | Signals what task is to be set out -> STORE in 'headerData'
    //  BPM[int] - BPM Value, followed with a value for the pulse   (Continuous)
    //  JND[int] - JND Testing, followed with a value for the pulse (Turns off after 15 seconds)
    //
    //  ON1      - Turn the module one
    //  OFF      - Turn the module off

    for (j = 1; j <= 3; j++) {        // Extract Header Code
      headerData[j - 1] = inData[j];  // headerData stores Header
    }
    headerData[j - 1] = '\0';         // End with null Character
    Serial.print("headerData: ");
    Serial.println(headerData);       // Print headerData

    // HEADER: ON - Turn on the device
    if (String(headerData) == "ONN") {
      Serial.print("Turned ON");

      int t = 0;
      char bpm_str[3];
      for (t = 4; t <= window_size; t++) {
        bpm_str[t - 4] = inData[t];
      }
      bpm_str[t] = '\0';
      bpmValue = atoi(bpm_str);               // Store value within bpm_value
      Serial.print("BPM Value: ");
      Serial.println(bpmValue);

    }

    // HEADER: OFF - Turn on the device
    if (String(headerData) == "OFF") {
      Serial.print("Turned OFF");
      //      state = false;
      bpmValue = 0;               //
    }

    // HEADER: BPM - Get the BPM value
    if (String(headerData) == "BPM") {       // Detect Header, this is active if it's reffers to BPM
      int t = 0;
      char bpm_str[3];
      for (t = 4; t <= window_size; t++) {
        bpm_str[t - 4] = inData[t];
      }
      bpm_str[t] = '\0';
      bpmValue = atoi(bpm_str);               // Store value within bpm_value
      Serial.print("BPM Value: ");
      Serial.println(bpmValue);
    }

    //HEADER: BTS - Get the BPM and start the Testing
    if (String(headerData) == "BTS") {       // Detect Header, this is active if it's reffers to BPM
      int t = 0;                             // Initialise to 0
      char bpm_str[3];
      for (t = 4; t <= window_size; t++) {
        bpm_str[t - 4] = inData[t];
      }
      bpm_str[t] = '\0';
      bpmValue = atoi(bpm_str);               // Store value within bpm_value
      Serial.print("BPM Value: ");
      Serial.println(bpmValue);
    }


    //HEADER: BTF - Get the BPM and Finish the Testing
    if (String(headerData) == "BTF") {       // Detect Header, this is active if it's reffers to BPM
      int t = 0;                             // Initialise to 0
      char bpm_str[3];
      for (t = 4; t <= window_size; t++) {
        bpm_str[t - 4] = inData[t];
      }
      bpm_str[t] = '\0';
      bpmValue = atoi(bpm_str);               // Store value within bpm_value
      Serial.print("BPM Value: ");
      Serial.println(bpmValue);
    }

    //HEADER: DIS - The module is connected the computer
    if (String(headerData) == "DIS") {
      Serial.print("Disconnected");
      //      state = false;  // Turn off the module
      bpmValue = 0;
    }



    // HEADER: JND - testing the JND of the module
    if (String(headerData) == "JND") {

      Serial.println("JND testing begin");
      int t = 0;                             // Initialise to 0
      char bpm_str[3];
      char responder[1];

      JND_testing = true;       // set it to true as we're testing the JND!

      for (t = 4; t <= window_size; t++) {
        bpm_str[t - 4] = inData[t];
      }

      bpm_str[t] = '\0';

      temp_test = atoi(bpm_str);               // Store value within bpm_value

      responder[0] = inData[7];               // Extract the order of the value

      bpmValue = 0; // turn it off first!!

      Serial.println(responder);


      char check_string[] = "S";

      int i = strcmp(responder, check_string);

      if (i == 0) {
        const_first = true;   // Set the constant first eqaul to True
        const_second = false;
      } else {
        const_first = false;  // Working
        const_second = true;
      }

      Serial.println(const_first);

      Serial.print("BPM Value: ");
      Serial.println(bpmValue);
      Serial.println(temp_test);
    }

    //HEADER: CON - The module has been disconnected from the computer
    if (String(headerData) == "CON") {
      Serial.print("Connected!");
      //      state = false;  // Turn On the module - LED notification
      //      Do appropriate setup
      // Flash Led to state connection is good

    }

    // REMOVE Everything from the buffer
    if (first_bytes >= BUFFER_SIZE - 1) {   // If the incoming byte count is more than our buffer...
      remaining_bytes = byte_count - (BUFFER_SIZE - 1);   // Reduce the bytes that we plan on handling to below the buffer size
    }
    for (i = 0; i < remaining_bytes; i++) {   // Remove remaining bytes from buffer
      inChar = serial_connection.read();
      Serial.print("Hello");
    }

  }


  double Pulse[] = { 0, 1.7, 4.5, 8.6, 13.8, 20, 27, 33, 40, 45, 50, 54, 56, 58, 59, 60, 59, 59, 58, 57, 56, 55, 54, 54, 53, 53, 52, 52, 51, 51, 51, 50, 49, 48, 47, 45, 43, 40, 38, 34, 31, 28, 26, 23, 21, 20, 19, 18.9, 18.7, 18.8, 19, 19, 20, 20, 20, 20, 20, 20, 20, 19, 18.7, 18.1, 17.5, 16.9, 16.3, 15.7, 15, 14.4, 13.7, 13.2, 12.7, 12.2, 11.7, 11.2, 10.6, 10, 9.5, 9, 8.6, 8.1, 7.8, 7.4, 7.1, 6.8, 6.5, 6.2, 6, 5.8, 5.5, 5.3, 5.1, 5.1, 5.1, 4.6, 4.5, 4.1, 3.7, 3.5, 3.4, 3.3, 3.3, 3.1, 3.1, 3.1, 3, 3, 3, 3, 2.8, 2.8, 2.7, 2.6, 2.5, 2.3, 2.2, 2, 1.7, 1.6, 1.4, 1.4, 1.3, 1, 0.5, 0 };

  int dataLength = sizeof(Pulse) / 4; // Divide by four bits to convert it into decimal
  int max_value = 60;                 // Highest BPM value recorded
  int analogue_gen = 254 / max_value; // Obtaining a value to be represented in the DAC
  


  if (JND_testing == true) {

    if (stage_one == 3) {
      stage_one = 0;
      const_first = false;

      if (jnd_counter <= 4) {
        const_second = true;
      }
      delay(100); // delay for a second
    }

    if (stage_two == 3) {
      stage_two = 0;
      const_second = false;
      if (jnd_counter <= 4) {
        const_first = true;
      }

      delay(100); // delay for a second
    }

    //    Serial.print("Jnd_counter ");
    //    Serial.println(jnd_counter);

    if (jnd_counter == 6) {         // Reset everything
      JND_testing = false;
      stage_one = 0;
      stage_two = 0;
      jnd_counter = 0;
      bpmValue = 0;
    }

    // Check which value is going first
    if (const_first == true) {
      bpmValue = temp_test;
      Serial.println("const_first");
      Serial.println(bpmValue);
      jnd_counter += 1;
      stage_one += 1;
    }

    if (const_second == true) {
      //      Serial.print(temp_test);

      bpmValue = 100;
      Serial.println("const_second");
      Serial.println(bpmValue);
      jnd_counter += 1;
      stage_two += 1;
    }

  }

  if (bpmValue != 0 ) {     // Active if the BPM value isn't zero | ON/OFF

    for (int t = 0; t <= dataLength; t++) {

      PORTD = analogue_gen * (Pulse[t] * 0.95);    // step through the Look-up-Table and multiply to get // Added percentage to controll the strength

      float bpm_val_per_min = 60 / bpmValue;   // 60 seconds divided by Incoming BPM Value, i.e 60/60pm = 1 per second, 60/120 = 0.5 per second
      // 1/1 = 1 per s,         1/0.5 = 2 per s.


      bpm_val_per_min_toSeconds = bpm_val_per_min * 1000;   // The bpm on the previous line needs upscaling to seconds for the delay function.

      delay(bpm_val_per_min_toSeconds / dataLength);
    }
  }

}
