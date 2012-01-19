"""Initialize Panda3D integration.

"""
import pyrokit


cdef extern from "nodePath.h":
    cdef cppclass NodePath:
        pass

cdef extern from "bootstrap.h":
    cdef void initializePanda3DSystem()
    cdef void createRocketInputHandler(NodePath*)
    cdef void updateContext(char*)


def framePreContext(context):
    updateContext(context.name)


def initializeSystem():
    initializePanda3DSystem()


def initializeInput(mouseWatcher):
    createInputHandler(mouseWatcher)
    if framePreContext not in pyrokit.manager.framePreContextCallbacks:
        pyrokit.manager.addFramePreContextCallback(framePreContext)


cdef createInputHandler(node):
    createRocketInputHandler(<NodePath*> <long> node.this)
