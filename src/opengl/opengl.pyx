"""Initialize the OpenGL render interface.

"""
import pyrokit


cdef extern from "ShellRenderInterfaceOpenGL.h":
    void startFrame(int, int)
    void endFrame()

cdef extern from "bootstrap.h":
    cdef void initializeOpenGLRenderer()


def framePreContext(context):
    startFrame(context.dimensions.x, context.dimensions.y)


def framePostContext(context):
    endFrame()


def initializeRenderer():
    initializeOpenGLRenderer()
    pyrokit.manager.addFramePreContextCallback(framePreContext)
    pyrokit.manager.addFramePostContextCallback(framePostContext)
