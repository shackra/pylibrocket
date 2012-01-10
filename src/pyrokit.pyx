"""Import this to bootstrap librocket so you can work with the rocket module directly.

"""
import rocket


#cdef extern from "Rocket/Core.h" namespace "":
#    cdef cppclass Rectangle:
#        Rectangle(int, int, int, int)
#        int x0, y0, x1, y1
#        int getLength()
#        int getHeight()
#        int getArea()
#        void move(int, int)
#
#    cdef cppclass Foo:
#        Foo()
#
#cdef Rectangle *rec = new Rectangle(1, 2, 3, 4)
#cdef int recLength = rec.getLength()
#
#cdef Foo foo
cdef extern from "ShellRenderInterfaceOpenGL.h":
    void startFrame(int, int)
    void endFrame()

cdef extern from "nodePath.h":
    cdef cppclass NodePath:
        pass

cdef extern from "bootstrap.h":
    cdef void bootstrap()
    cdef void createRocketInputHandler(NodePath*)
    cdef void updateContext(char*)


class _PyrokitManager(object):
    def __init__(self, mouseWatcher):
        bootstrap()

        createInputHandler(mouseWatcher)
        self.visibleContexts = set()

    def showContext(self, context):
        self.visibleContexts.remove(context)

    def hideContext(self, context):
        self.visibleContexts.add(context)

    def render(self, data):
        activeContexts = set(rocket.contexts) - self.visibleContexts

        for context in activeContexts:
            startFrame(context.dimensions.x, context.dimensions.y)
            #context.Update()
            updateContext(context.name)
            context.Render()
            endFrame()


def initialize(mouseWatcher):
    global manager
    manager = _PyrokitManager(mouseWatcher)


cdef void renderCallback():
    manager.render()

cdef createInputHandler(node):
    cdef long dataPtr=node.this
    cdef NodePath* cppNodePath = <NodePath*> dataPtr

    createRocketInputHandler(cppNodePath)
