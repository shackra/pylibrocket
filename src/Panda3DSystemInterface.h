#ifndef __PANDA3DSYSTEMINTERFACE_H__
#define __PANDA3DSYSTEMINTERFACE_H__

#include <ctime>

#include <Rocket/Core/SystemInterface.h>

#include "panda3d/pointerTo.h"
#include "panda3d/clockObject.h"


class Panda3DSystemInterface : public Rocket::Core::SystemInterface
{
public:
    // Constructor
	Panda3DSystemInterface();

    virtual float GetElapsedTime();

private:
	PT(ClockObject) globalClock;
}; // end Panda3DSystemInterface


#endif // __PANDA3DSYSTEMINTERFACE_H__
