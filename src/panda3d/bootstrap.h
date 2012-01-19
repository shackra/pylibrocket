#ifndef __PYROKIT_PANDA3D_BOOTSTRAP_H__
#define __PYROKIT_PANDA3D_BOOTSTRAP_H__


struct Panda3DSystemInterface;
struct RocketInputHandler;
struct NodePath;


extern Panda3DSystemInterface* panda3dSystem;
extern RocketInputHandler* inputHandler;


void initializePanda3DSystem();
void createRocketInputHandler(NodePath* parent);
void updateContext(char* contextName);


#endif // __PYROKIT_PANDA3D_BOOTSTRAP_H__
