#ifndef __PYROKIT_BOOTSTRAP_H__
#define __PYROKIT_BOOTSTRAP_H__


struct Panda3DSystemInterface;
struct ShellRenderInterfaceOpenGL;
struct RocketInputHandler;
struct NodePath;


extern Panda3DSystemInterface* panda3dSystem;
extern ShellRenderInterfaceOpenGL* openglRenderer;
extern RocketInputHandler* inputHandler;


void bootstrap();
void createRocketInputHandler(NodePath* parent);
void updateContext(char* contextName);


#endif // __PYROKIT_BOOTSTRAP_H__
