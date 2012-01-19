#include <cstdio>

#include <Rocket/Core.h>
#include <Rocket/Core/StringBase.h>

#include "pandaFramework.h"
#include "pandaSystem.h"
#include "mouseAndKeyboard.h"

#include "Panda3DSystemInterface.h"
#include "rocketInputHandler.h"
#include "bootstrap.h"


Panda3DSystemInterface* panda3dSystem = NULL;
RocketInputHandler* inputHandler = NULL;

void initializePanda3DSystem()
{
    panda3dSystem = new Panda3DSystemInterface;
    Rocket::Core::SetSystemInterface(panda3dSystem);
} // end initializePanda3DSystem

void createRocketInputHandler(NodePath* parent)
{
	// Create our input handler datanode
	inputHandler = new RocketInputHandler("Pyrokit Input Handler");
	parent->attach_new_node(inputHandler);
} // end createRocketInputHandler

void updateContext(char* contextName)
{
	if(inputHandler != NULL)
	{
		//TODO: Figure out what these values should be.
		int xoffs = 0;
		int yoffs = 0;

		// Get the c++ version of the context
		Rocket::Core::StringBase<char> name = Rocket::Core::StringBase<char>(contextName);
		Rocket::Core::Context* context = Rocket::Core::GetContext(name);

		if(context == NULL)
		{
			printf("*** Context \"%s\" is null!\n", contextName);
			fflush(stdout);
		} // end if

		// Update the context
		inputHandler->update_context(context, xoffs, yoffs);
	} // end if
} // end updateContext
