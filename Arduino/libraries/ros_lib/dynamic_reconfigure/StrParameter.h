#ifndef _ROS_dynamic_reconfigure_StrParameter_h
#define _ROS_dynamic_reconfigure_StrParameter_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"

namespace dynamic_reconfigure
{

  class StrParameter : public ros::Msg
  {
    public:
      char * name;
      char * value;

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      uint32_t * length_name = (uint32_t *)(outbuffer + offset);
      *length_name = strlen( (const char*) this->name);
      offset += 4;
      memcpy(outbuffer + offset, this->name, *length_name);
      offset += *length_name;
      uint32_t * length_value = (uint32_t *)(outbuffer + offset);
      *length_value = strlen( (const char*) this->value);
      offset += 4;
      memcpy(outbuffer + offset, this->value, *length_value);
      offset += *length_value;
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      uint32_t length_name = *(uint32_t *)(inbuffer + offset);
      offset += 4;
      for(unsigned int k= offset; k< offset+length_name; ++k){
          inbuffer[k-1]=inbuffer[k];
      }
      inbuffer[offset+length_name-1]=0;
      this->name = (char *)(inbuffer + offset-1);
      offset += length_name;
      uint32_t length_value = *(uint32_t *)(inbuffer + offset);
      offset += 4;
      for(unsigned int k= offset; k< offset+length_value; ++k){
          inbuffer[k-1]=inbuffer[k];
      }
      inbuffer[offset+length_value-1]=0;
      this->value = (char *)(inbuffer + offset-1);
      offset += length_value;
     return offset;
    }

    const char * getType(){ return "dynamic_reconfigure/StrParameter"; };
    const char * getMD5(){ return "bc6ccc4a57f61779c8eaae61e9f422e0"; };

  };

}
#endif