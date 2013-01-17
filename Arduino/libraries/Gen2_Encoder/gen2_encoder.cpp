/*
Library for reading the optical encoders on Gen2_Robots
Author: Brian Pappas
Last Update: 12/18/2012
*/

#include "Arduino.h"
#include "gen2_encoder.h"

gen2_encoder::gen2_encoder(int ch1Pin, int ch2Pin, boolean m_direction)
{
  pinMode(ch1Pin, INPUT);
  pinMode(ch2Pin, INPUT);
  _ch1Pin = ch1Pin;
  _ch2Pin = ch2Pin;
  _odometer = 0;
  _delta = 0;
  _oldodom = 0;
  m_dir = m_direction;
}

//Increment/Decrement Encoder Tick Count
void gen2_encoder::count()
{
  if(m_dir == true) {
  if(digitalRead(_ch2Pin) == HIGH)
  {
    _odometer++;
  }
  else{
    _odometer--;
  }
  
  }
  else {
     if(digitalRead(_ch2Pin) == HIGH)
  {
    _odometer--;
  }
  else{
    _odometer++;
  }
    
  }
}

//Return Total Tick Count
int gen2_encoder::totaldistance()
{
  return _odometer;
}
