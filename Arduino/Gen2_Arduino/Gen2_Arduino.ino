#include <gen2_motor.h>
#include <gen2_encoder.h>

//Define Pin Connection for Encoders.
const int encoderLeft_CH1 = 19; //<-left motor interrupt
const int encoderLeft_CH2 = 22; //<-left motor direction
const int encoderRight_CH1 = 18;//<-right motor interrupt
const int encoderRight_CH2 = 23;//<-right motor direction 

//Define Pin Connections for Motor Controller
const int motorLeft_Enable = 2;
const int motorLeft_I1 = 25;
const int motorLeft_I2 = 24;
const int motorRight_Enable = 3;
const int motorRight_I1 = 29;
const int motorRight_I2 = 28;


//Intialize Encoder Objects
  gen2_encoder eright(encoderRight_CH1, encoderRight_CH2, true);
  gen2_encoder eleft(encoderLeft_CH1, encoderLeft_CH2, true);
  
//Intialize Motor Object
  gen2_motor m(motorRight_Enable, motorRight_I1, motorRight_I2,motorLeft_Enable, motorLeft_I1, motorLeft_I2);

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
  delay(250);
  encoder_test();
  motor_test();
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

void motor_test()
{
  m.left_mspeed(75);
  m.right_mspeed(75);
  m.right_backward();
  m.left_backward();
 
}
