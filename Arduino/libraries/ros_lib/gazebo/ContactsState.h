#ifndef _ROS_gazebo_ContactsState_h
#define _ROS_gazebo_ContactsState_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"
#include "std_msgs/Header.h"
#include "gazebo/ContactState.h"

namespace gazebo
{

  class ContactsState : public ros::Msg
  {
    public:
      std_msgs::Header header;
      uint8_t states_length;
      gazebo::ContactState st_states;
      gazebo::ContactState * states;

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      offset += this->header.serialize(outbuffer + offset);
      *(outbuffer + offset++) = states_length;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = 0;
      *(outbuffer + offset++) = 0;
      for( uint8_t i = 0; i < states_length; i++){
      offset += this->states[i].serialize(outbuffer + offset);
      }
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      offset += this->header.deserialize(inbuffer + offset);
      uint8_t states_lengthT = *(inbuffer + offset++);
      if(states_lengthT > states_length)
        this->states = (gazebo::ContactState*)realloc(this->states, states_lengthT * sizeof(gazebo::ContactState));
      offset += 3;
      states_length = states_lengthT;
      for( uint8_t i = 0; i < states_length; i++){
      offset += this->st_states.deserialize(inbuffer + offset);
        memcpy( &(this->states[i]), &(this->st_states), sizeof(gazebo::ContactState));
      }
     return offset;
    }

    const char * getType(){ return "gazebo/ContactsState"; };
    const char * getMD5(){ return "9d29ce6da289d3d303cc64b4cfdd0e84"; };

  };

}
#endif