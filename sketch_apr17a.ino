#include <Servo.h>

const int numPins = 5;    // number of PWM pins
const int pwmPins[numPins] = {11, 10, 9, 5, 6};  // list of PWM pins
float angles[numPins] = {};    // array to store angle values
Servo servos[numPins];    // array of servo objects


void setup() {
  Serial.begin(9600);
  // attach servo objects to PWM pins
  for (int i = 0; i < numPins; i++) {
    servos[i].attach(pwmPins[i]);
  }
}

byte tmp[4];

void loop() {
  // read 5 float values from serial port
  for (int i = 0; i < numPins; i++) {
    while (Serial.available() < 4);    // wait for input
    for (int j = 0; j < 4; j++) {
       tmp[j] = Serial.read();
    }
    angles[i] = *((float*)tmp);
  }

  // map angle values to servo positions and write to PWM pins
  for (int i = 0; i < numPins; i++) {
    int servoPosition = map(angles[i], 0, 180, 0, 180);
    servos[i].write(servoPosition);
  }
}
