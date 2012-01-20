"""Initialize Panda3D integration.

"""
import pyrokit


cdef extern from "cullTraverser.h":
    cdef cppclass CullTraverser:
        pass

cdef extern from "nodePath.h":
    cdef cppclass NodePath:
        pass

cdef extern from "Rocket/Core/Core.h" namespace "Rocket::Core":
    cdef cppclass Context:
        pass

    cdef cppclass RenderInterface:
        pass

    cdef void SetRenderInterface(RenderInterface* renderer)

cdef extern from "rocketRenderInterface.h":
    cdef cppclass RocketRenderInterface:
       void render(Context* context, CullTraverser *trav) 

cdef extern from "bootstrap.h":
    cdef void initializePanda3DSystem()
    cdef void createRocketInputHandler(NodePath*)
    cdef void updateContext(char*)

cdef RocketRenderInterface* renderer

def framePreContext(context):
    updateContext(context.name)


def initializeSystem():
    initializePanda3DSystem()


cpdef initializeRenderer():
    global renderer
    renderer = new RocketRenderInterface()
    SetRenderInterface(<RenderInterface*> renderer)


def initializeInput(mouseWatcher):
    createInputHandler(mouseWatcher)
    if framePreContext not in pyrokit.manager.framePreContextCallbacks:
        pyrokit.manager.addFramePreContextCallback(framePreContext)


cdef createInputHandler(node):
    createRocketInputHandler(<NodePath*> <long> node.this)
