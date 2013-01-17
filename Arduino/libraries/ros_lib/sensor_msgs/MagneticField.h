#ifndef ros_sensor_msgs_MagneticField_h
#define ros_sensor_msgs_MagneticField_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "../ros/msg.h"
#include "std_msgs/Header.h"
#include "geometry_msgs/Vector3.h"

namespace sensor_msgs
{

  class MagneticField : public ros::Msg
  {
    public:
      std_msgs::Header header;
      geometry_msgs::Vector3 magnetic_field;
      float magnetic_field_covariance[9];

    virtual int serialize(unsigned char *outbuffer)
    {
      int offset = 0;
      offset += this->header.serialize(outbuffer + offset);
      offset += this->magnetic_field.serialize(outbuffer + offset);
      unsigned char * magnetic_field_covariance_val = (unsigned char *) this->magnetic_field_covariance;
      for( unsigned char i = 0; i < 9; i++){
      long * val_magnetic_field_covariancei = (long *) &(this->magnetic_field_covariance[i]);
      long exp_magnetic_field_covariancei = (((*val_magnetic_field_covariancei)>>23)&255);
      if(exp_magnetic_field_covariancei != 0)
        exp_magnetic_field_covariancei += 1023-127;
      long sig_magnetic_field_covariancei = *val_magnetic_field_covariancei;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = (sig_magnetic_field_covariancei<<5) & 0xff;
      *(outbuffer + offset++) = (sig_magnetic_field_covariancei>>3) & 0xff;
      *(outbuffer + offset++) = (sig_magnetic_field_covariancei>>11) & 0xff;
      *(outbuffer + offset++) = ((exp_magnetic_field_covariancei<<4) & 0xF0) | ((sig_magnetic_field_covariancei>>19)&0x0F);
      *(outbuffer + offset++) = (exp_magnetic_field_covariancei>>4) & 0x7F;
      if(this->magnetic_field_covariance[i] < 0) *(outbuffer + offset -1) |= 0x80;
      }
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      offset += this->header.deserialize(inbuffer + offset);
      offset += this->magnetic_field.deserialize(inbuffer + offset);
      unsigned char * magnetic_field_covariance_val = (unsigned char *) this->magnetic_field_covariance;
      for( unsigned char i = 0; i < 9; i++){
      unsigned long * val_magnetic_field_covariancei = (unsigned long*) &(this->magnetic_field_covariance[i]);
      offset += 3;
      *val_magnetic_field_covariancei = ((unsigned long)(*(inbuffer + offset++))>>5 & 0x07);
      *val_magnetic_field_covariancei |= ((unsigned long)(*(inbuffer + offset++)) & 0xff)<<3;
      *val_magnetic_field_covariancei |= ((unsigned long)(*(inbuffer + offset++)) & 0xff)<<11;
      *val_magnetic_field_covariancei |= ((unsigned long)(*(inbuffer + offset)) & 0x0f)<<19;
      unsigned long exp_magnetic_field_covariancei = ((unsigned long)(*(inbuffer + offset++))&0xf0)>>4;
      exp_magnetic_field_covariancei |= ((unsigned long)(*(inbuffer + offset)) & 0x7f)<<4;
      if(exp_magnetic_field_covariancei !=0)
        *val_magnetic_field_covariancei |= ((exp_magnetic_field_covariancei)-1023+127)<<23;
      if( ((*(inbuffer+offset++)) & 0x80) > 0) this->magnetic_field_covariance[i] = -this->magnetic_field_covariance[i];
      }
     return offset;
    }

    const char * getType(){ return "sensor_msgs/MagneticField"; };

  };

}
#endif