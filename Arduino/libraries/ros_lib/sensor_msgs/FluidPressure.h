#ifndef ros_sensor_msgs_FluidPressure_h
#define ros_sensor_msgs_FluidPressure_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "../ros/msg.h"
#include "std_msgs/Header.h"

namespace sensor_msgs
{

  class FluidPressure : public ros::Msg
  {
    public:
      std_msgs::Header header;
      float fluid_pressure;
      float variance;

    virtual int serialize(unsigned char *outbuffer)
    {
      int offset = 0;
      offset += this->header.serialize(outbuffer + offset);
      long * val_fluid_pressure = (long *) &(this->fluid_pressure);
      long exp_fluid_pressure = (((*val_fluid_pressure)>>23)&255);
      if(exp_fluid_pressure != 0)
        exp_fluid_pressure += 1023-127;
      long sig_fluid_pressure = *val_fluid_pressure;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = (sig_fluid_pressure<<5) & 0xff;
      *(outbuffer + offset++) = (sig_fluid_pressure>>3) & 0xff;
      *(outbuffer + offset++) = (sig_fluid_pressure>>11) & 0xff;
      *(outbuffer + offset++) = ((exp_fluid_pressure<<4) & 0xF0) | ((sig_fluid_pressure>>19)&0x0F);
      *(outbuffer + offset++) = (exp_fluid_pressure>>4) & 0x7F;
      if(this->fluid_pressure < 0) *(outbuffer + offset -1) |= 0x80;
      long * val_variance = (long *) &(this->variance);
      long exp_variance = (((*val_variance)>>23)&255);
      if(exp_variance != 0)
        exp_variance += 1023-127;
      long sig_variance = *val_variance;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = (sig_variance<<5) & 0xff;
      *(outbuffer + offset++) = (sig_variance>>3) & 0xff;
      *(outbuffer + offset++) = (sig_variance>>11) & 0xff;
      *(outbuffer + offset++) = ((exp_variance<<4) & 0xF0) | ((sig_variance>>19)&0x0F);
      *(outbuffer + offset++) = (exp_variance>>4) & 0x7F;
      if(this->variance < 0) *(outbuffer + offset -1) |= 0x80;
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      offset += this->header.deserialize(inbuffer + offset);
      unsigned long * val_fluid_pressure = (unsigned long*) &(this->fluid_pressure);
      offset += 3;
      *val_fluid_pressure = ((unsigned long)(*(inbuffer + offset++))>>5 & 0x07);
      *val_fluid_pressure |= ((unsigned long)(*(inbuffer + offset++)) & 0xff)<<3;
      *val_fluid_pressure |= ((unsigned long)(*(inbuffer + offset++)) & 0xff)<<11;
      *val_fluid_pressure |= ((unsigned long)(*(inbuffer + offset)) & 0x0f)<<19;
      unsigned long exp_fluid_pressure = ((unsigned long)(*(inbuffer + offset++))&0xf0)>>4;
      exp_fluid_pressure |= ((unsigned long)(*(inbuffer + offset)) & 0x7f)<<4;
      if(exp_fluid_pressure !=0)
        *val_fluid_pressure |= ((exp_fluid_pressure)-1023+127)<<23;
      if( ((*(inbuffer+offset++)) & 0x80) > 0) this->fluid_pressure = -this->fluid_pressure;
      unsigned long * val_variance = (unsigned long*) &(this->variance);
      offset += 3;
      *val_variance = ((unsigned long)(*(inbuffer + offset++))>>5 & 0x07);
      *val_variance |= ((unsigned long)(*(inbuffer + offset++)) & 0xff)<<3;
      *val_variance |= ((unsigned long)(*(inbuffer + offset++)) & 0xff)<<11;
      *val_variance |= ((unsigned long)(*(inbuffer + offset)) & 0x0f)<<19;
      unsigned long exp_variance = ((unsigned long)(*(inbuffer + offset++))&0xf0)>>4;
      exp_variance |= ((unsigned long)(*(inbuffer + offset)) & 0x7f)<<4;
      if(exp_variance !=0)
        *val_variance |= ((exp_variance)-1023+127)<<23;
      if( ((*(inbuffer+offset++)) & 0x80) > 0) this->variance = -this->variance;
     return offset;
    }

    const char * getType(){ return "sensor_msgs/FluidPressure"; };

  };

}
#endif