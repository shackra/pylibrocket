#ifndef __PYROKIT_BOOTSTRAP_H__
#define __PYROKIT_BOOTSTRAP_H__


struct Panda3DSystemInterface;
struct ShellRenderInterfaceOpenGL;


extern Panda3DSystemInterface* panda3dSystem;
extern ShellRenderInterfaceOpenGL* openglRenderer;


void bootstrap();


#endif // __PYROKIT_BOOTSTRAP_H__
