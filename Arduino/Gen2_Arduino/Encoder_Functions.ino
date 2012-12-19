Encoder::Encoder(int ch1Pin, int ch2Pin, boolean m_direction)
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

void Encoder::count()
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

int Encoder::totaldistance()
{
  return _odometer;
}

int Encoder::deltadistance()
{
  _delta = _odometer-_oldodom;
  _odometer = _oldodom;
  return _delta;
}
