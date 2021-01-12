//0: open
//1023: closed
#include <Servo.h>

String inString = "0";
int val = 0;
int inChar = 0;
int cur_mot = 0;
int maxA = 1700;
int minA = 1400;
int maxB = 1650;
int minB = 1400;

Servo servoA;
Servo servoB;

void setup() {
  
  Serial.begin(115200);
  while (!Serial) {
    ;
  }

  Serial.println("Valve Beginning");
  Serial.println();

  // 245.1 hz
  //TCCR2B = TCCR2B & B11111000 | B00000110; 
  // 30.64hz
  TCCR2B = TCCR2B & B11111000 | B00000111;

  servoA.attach(2);
  servoB.attach(3);

  servoA.writeMicroseconds(maxA);
  servoB.writeMicroseconds(maxB);


  val = inString.toInt();
}

void loop() {
  while (Serial.available() > 0) {
    inChar = Serial.read();
    if (isDigit(inChar)) {
      inString += (char)inChar;
    }

    if (inChar == 'a') {
      cur_mot = 0;
    }

    if (inChar == 'b') {
      cur_mot = 1;
    }

    if (inChar == '\n') {
      val = inString.toInt();     // scale it to use it with the servo (value between 0 and 180)
      if (cur_mot == 0) {
        if (val > maxA) { val = maxA; }
        if (val < minA) { val = minA; }
        servoA.writeMicroseconds(val);
      }
      if (cur_mot == 1)
        if (val > maxB) { val = maxB; }
        if (val < minB) { val = minB; }
        servoB.writeMicroseconds(val);
      inString = "";
    }
  }
}
