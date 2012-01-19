#include "Panda3DSystemInterface.h"


// Constructor
Panda3DSystemInterface::Panda3DSystemInterface() :
	globalClock(ClockObject::get_global_clock())
{
} // end Panda3DSystemInterface

float Panda3DSystemInterface::GetElapsedTime()
{
	return (float) globalClock->get_real_time();
} // end GetElapsedTime
