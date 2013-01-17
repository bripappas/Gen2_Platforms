#ifndef ros_std_msgs_Float32_h
#define ros_std_msgs_Float32_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "../ros/msg.h"

namespace std_msgs
{

  class Float32 : public ros::Msg
  {
    public:
      float data;

    virtual int serialize(unsigned char *outbuffer)
    {
      int offset = 0;
      union {
        float real;
        unsigned long base;
      } u_data;
      u_data.real = this->data;
      *(outbuffer + offset + 0) = (u_data.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_data.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_data.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_data.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->data);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      union {
        float real;
        unsigned long base;
      } u_data;
      u_data.base = 0;
      u_data.base |= ((typeof(u_data.base)) (*(inbuffer + offset + 0))) << (8 * 0);
      u_data.base |= ((typeof(u_data.base)) (*(inbuffer + offset + 1))) << (8 * 1);
      u_data.base |= ((typeof(u_data.base)) (*(inbuffer + offset + 2))) << (8 * 2);
      u_data.base |= ((typeof(u_data.base)) (*(inbuffer + offset + 3))) << (8 * 3);
      this->data = u_data.real;
      offset += sizeof(this->data);
     return offset;
    }

    const char * getType(){ return "std_msgs/Float32"; };

  };

}
#endif