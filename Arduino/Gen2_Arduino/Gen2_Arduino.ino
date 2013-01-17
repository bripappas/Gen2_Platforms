#include <gen2_encoder.h>

//Define Pin Connection for Encoders.
const int encoderLeft_CH1 = 19; //<-left motor interrupt
const int encoderLeft_CH2 = 22; //<-left motor direction
const int encoderRight_CH1 = 18;//<-right motor interrupt
const int encoderRight_CH2 = 23;//<-right motor direction 


//Intialize Encoder Objects
  gen2_encoder eright(encoderRight_CH1, encoderRight_CH2, true);
  gen2_encoder eleft(encoderLeft_CH1, encoderLeft_CH2, true);

void setup()
{
  //Interrupt Initialization for Encoder Counting
  attachInterrupt(5, countright, RISING);
  attachInterrupt(4, countleft, RISING);
  
  //Start serial interface
  Serial.begin(9600);
}

void loop()
{
  delay(100);
  encoder_test();
}

//Encoder Interrupt Function Calls------------------------------------------------------
void countright()
{
  eright.count();
}

void countleft()
{
  eleft.count();
}

void encoder_test()
{
  Serial.print("Right Odom: ");
  Serial.println(eright.totaldistance());
  Serial.print("Left Odom: ");
  Serial.println(eleft.totaldistance());
}
