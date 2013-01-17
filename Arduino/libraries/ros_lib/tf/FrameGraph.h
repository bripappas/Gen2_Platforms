#ifndef ros_SERVICE_FrameGraph_h
#define ros_SERVICE_FrameGraph_h
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "../ros/msg.h"

namespace tf
{

static const char FRAMEGRAPH[] = "tf/FrameGraph";

  class FrameGraphRequest : public ros::Msg
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

    const char * getType(){ return FRAMEGRAPH; };

  };

  class FrameGraphResponse : public ros::Msg
  {
    public:
      char * dot_graph;

    virtual int serialize(unsigned char *outbuffer)
    {
      int offset = 0;
      long * length_dot_graph = (long *)(outbuffer + offset);
      *length_dot_graph = strlen( (const char*) this->dot_graph);
      offset += 4;
      memcpy(outbuffer + offset, this->dot_graph, *length_dot_graph);
      offset += *length_dot_graph;
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      uint32_t length_dot_graph = *(uint32_t *)(inbuffer + offset);
      offset += 4;
      for(unsigned int k= offset; k< offset+length_dot_graph; ++k){
          inbuffer[k-1]=inbuffer[k];
           }
      inbuffer[offset+length_dot_graph-1]=0;
      this->dot_graph = (char *)(inbuffer + offset-1);
      offset += length_dot_graph;
     return offset;
    }

    const char * getType(){ return FRAMEGRAPH; };

  };

}
#endif