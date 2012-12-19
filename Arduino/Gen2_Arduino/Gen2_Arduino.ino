//Define Pin Connection for Encoders.
const int encoderLeft_CH1 = 19; //<-left motor interrupt
const int encoderLeft_CH2 = 22; //<-left motor direction
const int encoderRight_CH1 = 18;//<-right motor interrupt
const int encoderRight_CH2 = 23;//<-right motor direction 

//Encoder class defintion.
class Encoder
{
  public:
    Encoder(int ch1Pin, int ch2Pin, boolean m_direction);
    void count();
    int totaldistance();
    int deltadistance();
  
  private:
    int _ch1Pin;
    int _ch2Pin;
    unsigned int _odometer;
    int _oldodom;
    int _delta;
    boolean m_dir;
};

//Intialize Encoder Objects
  Encoder eright(encoderRight_CH1, encoderRight_CH2, true);
  Encoder eleft(encoderLeft_CH1, encoderLeft_CH2, false);

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
  encoder_test();
}

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
