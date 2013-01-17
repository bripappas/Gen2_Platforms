#ifndef ros_SERVICE_SelfTest_h
#define ros_SERVICE_SelfTest_h
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "../ros/msg.h"
#include "diagnostic_msgs/DiagnosticStatus.h"

namespace diagnostic_msgs
{

static const char SELFTEST[] = "diagnostic_msgs/SelfTest";

  class SelfTestRequest : public ros::Msg
  {
    public:

    virtual int serialize(unsigned char *outbuffer)
    {
      int offset = 0;
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
     return offset;
    }

    const char * getType(){ return SELFTEST; };

  };

  class SelfTestResponse : public ros::Msg
  {
    public:
      char * id;
      unsigned char passed;
      unsigned char status_length;
      diagnostic_msgs::DiagnosticStatus st_status;
      diagnostic_msgs::DiagnosticStatus * status;

    virtual int serialize(unsigned char *outbuffer)
    {
      int offset = 0;
      long * length_id = (long *)(outbuffer + offset);
      *length_id = strlen( (const char*) this->id);
      offset += 4;
      memcpy(outbuffer + offset, this->id, *length_id);
      offset += *length_id;
      union {
        unsigned char real;
        unsigned char base;
      } u_passed;
      u_passed.real = this->passed;
      *(outbuffer + offset + 0) = (u_passed.base >> (8 * 0)) & 0xFF;
      offset += sizeof(this->passed);
      *(outbuffer + offset++) = status_length;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = 0;
      for( unsigned char i = 0; i < status_length; i++){
      offset += this->status[i].serialize(outbuffer + offset);
      }
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      uint32_t length_id = *(uint32_t *)(inbuffer + offset);
      offset += 4;
      for(unsigned int k= offset; k< offset+length_id; ++k){
          inbuffer[k-1]=inbuffer[k];
           }
      inbuffer[offset+length_id-1]=0;
      this->id = (char *)(inbuffer + offset-1);
      offset += length_id;
      union {
        unsigned char real;
        unsigned char base;
      } u_passed;
      u_passed.base = 0;
      u_passed.base |= ((typeof(u_passed.base)) (*(inbuffer + offset + 0))) << (8 * 0);
      this->passed = u_passed.real;
      offset += sizeof(this->passed);
      unsigned char status_lengthT = *(inbuffer + offset++);
      if(status_lengthT > status_length)
        this->status = (diagnostic_msgs::DiagnosticStatus*)realloc(this->status, status_lengthT * sizeof(diagnostic_msgs::DiagnosticStatus));
      offset += 3;
      status_length = status_lengthT;
      for( unsigned char i = 0; i < status_length; i++){
      offset += this->st_status.deserialize(inbuffer + offset);
        memcpy( &(this->status[i]), &(this->st_status), sizeof(diagnostic_msgs::DiagnosticStatus));
      }
     return offset;
    }

    const char * getType(){ return SELFTEST; };

  };

}
#endif