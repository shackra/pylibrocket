#include <cstdio>

#include <Rocket/Core.h>

#include "ShellRenderInterfaceOpenGL.h"
#include "bootstrap.h"


ShellRenderInterfaceOpenGL* openglRenderer = NULL;

void initializeOpenGLRenderer()
{
    openglRenderer = new ShellRenderInterfaceOpenGL;
	Rocket::Core::SetRenderInterface(openglRenderer);
} // end initializeOpenGLRenderer
