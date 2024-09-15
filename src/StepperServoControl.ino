#include <Stepper.h>
#include <Servo.h>

Servo myservo;

const int stepsPerRevolution = 2048;

Stepper myStepper = Stepper(stepsPerRevolution, 8, 10, 9, 11);

char move[2];

int pos = 1; //0, 1, 2, 3 for positions of trashcan

void setup() {
  Serial.begin(115200);

  myservo.attach(5); 
  myservo.write(60); 

}

void loop() {

  while(Serial.available() > 0)
  {

    // Read a character from the serial input
    int size = Serial.readBytes(move, 1);

    move[1] = '\0';

    // Convert the character to an integer
    int num = move[0] - '0';  // Converts char '1' to int 1, etc.

    int diff = pos - num;

    if(num == 5) {
       delay(1000); 

      myservo.write(140); 

      delay(10000); 

      myservo.write(60); 
    } 

    if(num > 0 && num < 5) {
      
      myStepper.setSpeed(13); 
      myStepper.step((stepsPerRevolution/4)*diff); 

      delay(1000); 

      myservo.write(140); 

      delay(1000); 

      myservo.write(60); 

      Serial.println(diff);
      Serial.println(num); 
      Serial.println("done");

      pos = num; 

    }
    
    Serial.flush(); 

  }
}