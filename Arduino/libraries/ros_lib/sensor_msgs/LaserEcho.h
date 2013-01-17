#ifndef ros_sensor_msgs_LaserEcho_h
#define ros_sensor_msgs_LaserEcho_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "../ros/msg.h"

namespace sensor_msgs
{

  class LaserEcho : public ros::Msg
  {
    public:
      unsigned char echoes_length;
      float st_echoes;
      float * echoes;

    virtual int serialize(unsigned char *outbuffer)
    {
      int offset = 0;
      *(outbuffer + offset++) = echoes_length;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = 0;
      for( unsigned char i = 0; i < echoes_length; i++){
      union {
        float real;
        unsigned long base;
      } u_echoesi;
      u_echoesi.real = this->echoes[i];
      *(outbuffer + offset + 0) = (u_echoesi.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_echoesi.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_echoesi.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_echoesi.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->echoes[i]);
      }
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      unsigned char echoes_lengthT = *(inbuffer + offset++);
      if(echoes_lengthT > echoes_length)
        this->echoes = (float*)realloc(this->echoes, echoes_lengthT * sizeof(float));
      offset += 3;
      echoes_length = echoes_lengthT;
      for( unsigned char i = 0; i < echoes_length; i++){
      union {
        float real;
        unsigned long base;
      } u_st_echoes;
      u_st_echoes.base = 0;
      u_st_echoes.base |= ((typeof(u_st_echoes.base)) (*(inbuffer + offset + 0))) << (8 * 0);
      u_st_echoes.base |= ((typeof(u_st_echoes.base)) (*(inbuffer + offset + 1))) << (8 * 1);
      u_st_echoes.base |= ((typeof(u_st_echoes.base)) (*(inbuffer + offset + 2))) << (8 * 2);
      u_st_echoes.base |= ((typeof(u_st_echoes.base)) (*(inbuffer + offset + 3))) << (8 * 3);
      this->st_echoes = u_st_echoes.real;
      offset += sizeof(this->st_echoes);
        memcpy( &(this->echoes[i]), &(this->st_echoes), sizeof(float));
      }
     return offset;
    }

    const char * getType(){ return "sensor_msgs/LaserEcho"; };

  };

}
#endif