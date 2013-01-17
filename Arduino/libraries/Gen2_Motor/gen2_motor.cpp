/*
Library for controlling the motors on the Gen2_Robots
Author: Brian Pappas
Last Update: 1/17/2013
*/

#include "Arduino.h"
#include "gen2_motor.h"

gen2_motor::gen2_motor(int right_enable, int right_I1, int right_I2, int left_enable, int left_I1, int left_I2)
{
  pinMode(right_enable, OUTPUT);
  pinMode(right_I1, OUTPUT);
  pinMode(right_I2, OUTPUT);
  _rightEnablePin = right_enable;
  _rightI1pin = right_I1;
  _rightI2pin = right_I2;
  _rightpwm = 0;
  analogWrite(right_enable, 0);
  
  pinMode(left_enable, OUTPUT);
  pinMode(left_I1, OUTPUT);
  pinMode(left_I2, OUTPUT);
  _leftEnablePin = left_enable;
  _leftI1pin = left_I1;
  _leftI2pin = left_I2;
  _leftpwm = 0;
  analogWrite(left_enable, 0);
  
  mstop();
}

//Functions to set motor direction
void gen2_motor::right_forward()
{
  digitalWrite(_rightI1pin, HIGH);
  digitalWrite(_rightI2pin, LOW);
}
void gen2_motor::left_forward()
{
  digitalWrite(_leftI1pin, HIGH);
  digitalWrite(_leftI2pin, LOW);
}
void gen2_motor::right_backward()
{
  digitalWrite(_rightI1pin, LOW);
  digitalWrite(_rightI2pin, HIGH);
}
void gen2_motor::left_backward()
{
  digitalWrite(_leftI1pin, LOW);
  digitalWrite(_leftI2pin, HIGH);
}

//Set right motor speed 0-255
void gen2_motor::right_mspeed(int value)
{
  	_rightpwm = value;
  	analogWrite(_rightEnablePin,_rightpwm);
}

//Set left motor speed 0-255
void gen2_motor::left_mspeed(int value)
{
	_leftpwm = value;
  	analogWrite(_leftEnablePin, _leftpwm);
}

//Hard stop both  motors
void gen2_motor::mstop()
{
  	digitalWrite(_rightI1pin, HIGH);
  	digitalWrite(_rightI2pin, HIGH);
  	digitalWrite(_leftI1pin, HIGH);
  	digitalWrite(_leftI2pin, HIGH);
}

//Hard stop right motor
void gen2_motor::right_mstop()
{
  	digitalWrite(_rightI1pin, HIGH);
  	digitalWrite(_rightI2pin, HIGH);
}

//Hard stop left motor
void gen2_motor::left_mstop()
{
  	digitalWrite(_leftI1pin, HIGH);
  	digitalWrite(_leftI2pin, HIGH);
}
