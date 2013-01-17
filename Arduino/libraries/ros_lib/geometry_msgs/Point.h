#ifndef ros_geometry_msgs_Point_h
#define ros_geometry_msgs_Point_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "../ros/msg.h"

namespace geometry_msgs
{

  class Point : public ros::Msg
  {
    public:
      float x;
      float y;
      float z;

    virtual int serialize(unsigned char *outbuffer)
    {
      int offset = 0;
      long * val_x = (long *) &(this->x);
      long exp_x = (((*val_x)>>23)&255);
      if(exp_x != 0)
        exp_x += 1023-127;
      long sig_x = *val_x;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = (sig_x<<5) & 0xff;
      *(outbuffer + offset++) = (sig_x>>3) & 0xff;
      *(outbuffer + offset++) = (sig_x>>11) & 0xff;
      *(outbuffer + offset++) = ((exp_x<<4) & 0xF0) | ((sig_x>>19)&0x0F);
      *(outbuffer + offset++) = (exp_x>>4) & 0x7F;
      if(this->x < 0) *(outbuffer + offset -1) |= 0x80;
      long * val_y = (long *) &(this->y);
      long exp_y = (((*val_y)>>23)&255);
      if(exp_y != 0)
        exp_y += 1023-127;
      long sig_y = *val_y;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = (sig_y<<5) & 0xff;
      *(outbuffer + offset++) = (sig_y>>3) & 0xff;
      *(outbuffer + offset++) = (sig_y>>11) & 0xff;
      *(outbuffer + offset++) = ((exp_y<<4) & 0xF0) | ((sig_y>>19)&0x0F);
      *(outbuffer + offset++) = (exp_y>>4) & 0x7F;
      if(this->y < 0) *(outbuffer + offset -1) |= 0x80;
      long * val_z = (long *) &(this->z);
      long exp_z = (((*val_z)>>23)&255);
      if(exp_z != 0)
        exp_z += 1023-127;
      long sig_z = *val_z;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = (sig_z<<5) & 0xff;
      *(outbuffer + offset++) = (sig_z>>3) & 0xff;
      *(outbuffer + offset++) = (sig_z>>11) & 0xff;
      *(outbuffer + offset++) = ((exp_z<<4) & 0xF0) | ((sig_z>>19)&0x0F);
      *(outbuffer + offset++) = (exp_z>>4) & 0x7F;
      if(this->z < 0) *(outbuffer + offset -1) |= 0x80;
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      unsigned long * val_x = (unsigned long*) &(this->x);
      offset += 3;
      *val_x = ((unsigned long)(*(inbuffer + offset++))>>5 & 0x07);
      *val_x |= ((unsigned long)(*(inbuffer + offset++)) & 0xff)<<3;
      *val_x |= ((unsigned long)(*(inbuffer + offset++)) & 0xff)<<11;
      *val_x |= ((unsigned long)(*(inbuffer + offset)) & 0x0f)<<19;
      unsigned long exp_x = ((unsigned long)(*(inbuffer + offset++))&0xf0)>>4;
      exp_x |= ((unsigned long)(*(inbuffer + offset)) & 0x7f)<<4;
      if(exp_x !=0)
        *val_x |= ((exp_x)-1023+127)<<23;
      if( ((*(inbuffer+offset++)) & 0x80) > 0) this->x = -this->x;
      unsigned long * val_y = (unsigned long*) &(this->y);
      offset += 3;
      *val_y = ((unsigned long)(*(inbuffer + offset++))>>5 & 0x07);
      *val_y |= ((unsigned long)(*(inbuffer + offset++)) & 0xff)<<3;
      *val_y |= ((unsigned long)(*(inbuffer + offset++)) & 0xff)<<11;
      *val_y |= ((unsigned long)(*(inbuffer + offset)) & 0x0f)<<19;
      unsigned long exp_y = ((unsigned long)(*(inbuffer + offset++))&0xf0)>>4;
      exp_y |= ((unsigned long)(*(inbuffer + offset)) & 0x7f)<<4;
      if(exp_y !=0)
        *val_y |= ((exp_y)-1023+127)<<23;
      if( ((*(inbuffer+offset++)) & 0x80) > 0) this->y = -this->y;
      unsigned long * val_z = (unsigned long*) &(this->z);
      offset += 3;
      *val_z = ((unsigned long)(*(inbuffer + offset++))>>5 & 0x07);
      *val_z |= ((unsigned long)(*(inbuffer + offset++)) & 0xff)<<3;
      *val_z |= ((unsigned long)(*(inbuffer + offset++)) & 0xff)<<11;
      *val_z |= ((unsigned long)(*(inbuffer + offset)) & 0x0f)<<19;
      unsigned long exp_z = ((unsigned long)(*(inbuffer + offset++))&0xf0)>>4;
      exp_z |= ((unsigned long)(*(inbuffer + offset)) & 0x7f)<<4;
      if(exp_z !=0)
        *val_z |= ((exp_z)-1023+127)<<23;
      if( ((*(inbuffer+offset++)) & 0x80) > 0) this->z = -this->z;
     return offset;
    }

    const char * getType(){ return "geometry_msgs/Point"; };

  };

}
#endif