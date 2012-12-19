/*
Library for reading the optical encoders on Gen2_Robots
Author: Brian Pappas
Last Update: 12/18/2012
*/

#ifndef gen2_gen2_encoder_h
#define gen2_gen2_encoder_h

#include "Arduino.h"

//gen2_encoder class defintion.
class gen2_encoder
{
  public:
    gen2_encoder(int ch1Pin, int ch2Pin, boolean m_direction);
    void count();
    int totaldistance();
  
  private:
    int _ch1Pin;
    int _ch2Pin;
    unsigned int _odometer;
    int _oldodom;
    int _delta;
    boolean m_dir;
};

#endif