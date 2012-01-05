#include <cstdio>

#include <Rocket/Core.h>

#include "pandaFramework.h"
#include "pandaSystem.h"

#include "ShellRenderInterfaceOpenGL.h"
#include "Panda3DSystemInterface.h"
#include "bootstrap.h"


Panda3DSystemInterface* panda3dSystem = NULL;
ShellRenderInterfaceOpenGL* openglRenderer = NULL;


void bootstrap()
{
    //LibRocket Setup Step 1 => System Interface
    panda3dSystem = new Panda3DSystemInterface;
    Rocket::Core::SetSystemInterface(panda3dSystem);

    //LibRocket Setup Step 2 => Render Interface
    openglRenderer = new ShellRenderInterfaceOpenGL;
	Rocket::Core::SetRenderInterface(openglRenderer);

    //LibRocket Setup Step 3 => Initialize
    Rocket::Core::Initialise();
} // end bootstrap
