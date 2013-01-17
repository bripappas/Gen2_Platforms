/*
Library for controlling the motors on the Gen2_Robots
Author: Brian Pappas
Last Update: 1/17/2013
*/

#ifndef gen2_gen2_motor_h
#define gen2_gen2_motor_h

#include "Arduino.h"

//gen2_motor class defintion.
class gen2_motor
{
  public:
    gen2_motor(int right_enable, int right_I1, int right_I2, int left_enable, int left_I1, int left_I2);
    void right_forward();
    void left_forward();
    void right_backward();
    void left_backward();
    void right_mspeed(int percent);
    void left_mspeed(int percent);
    void mstop();
    void right_mstop();
    void left_mstop();
  
  private:
    int _rightEnablePin;
    int _rightI1pin;
    int _rightI2pin;
    int _rightpwm;
    int _leftEnablePin;
    int _leftI1pin;
    int _leftI2pin;
    int _leftpwm;
};

#endif