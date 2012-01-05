import os
from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, PythonCallbackObject, CallbackNode

# OpenGL imports
import OpenGL.GL

import pyrokit

import rocket


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Disable the camera trackball controls.
        self.disableMouse()

        self.loadModels()

        pyrokit.initialize()

        self.rocketContext = rocket.CreateContext('main', rocket.Vector2i(self.win.getXSize(), self.win.getYSize()))

        print
        print "Contexts:"
        for context in rocket.contexts:
            print "  ", context.name
        print

        os.chdir(os.path.dirname(__file__))
        self.rocketContext.LoadDocument('data/demo.rml').Show()

        rocketCB = PythonCallbackObject(self.renderCallback)
        self.cbNode = CallbackNode("Rocket")
        self.cbNode.setDrawCallback(rocketCB)
        self.render2d.attachNewNode(self.cbNode)

        base.accept('window-event', self.windowEvent)

    def loadModels(self):
        # Load the environment model.
        self.environ = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.environ.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.environ.setScale(0.25, 0.25, 0.25)
        self.environ.setPos(-8, 42, 0)

        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        # Load and transform the panda actor.
        self.pandaActor = Actor("models/panda-model",
                {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        # Loop its animation.
        self.pandaActor.loop("walk")

        # Create the four lerp intervals needed for the panda to
        # walk back and forth.
        pandaPosInterval1 = self.pandaActor.posInterval(13, Point3(0, -10, 0), startPos=Point3(0, 10, 0))
        pandaPosInterval2 = self.pandaActor.posInterval(13, Point3(0, 10, 0), startPos=Point3(0, -10, 0))
        pandaHprInterval1 = self.pandaActor.hprInterval(3, Point3(180, 0, 0), startHpr=Point3(0, 0, 0))
        pandaHprInterval2 = self.pandaActor.hprInterval(3, Point3(0, 0, 0), startHpr=Point3(180, 0, 0))

        # Create and play the sequence that coordinates the intervals.
        self.pandaPace = Sequence(pandaPosInterval1,
                pandaHprInterval1,
                pandaPosInterval2,
                pandaHprInterval2,
                name="pandaPace")
        self.pandaPace.loop()

    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

    def windowEvent(self, window):
        self.rocketContext.dimensions = rocket.Vector2i(window.getXSize(), window.getYSize())

    def renderCallback(self, data):
        self.rocketContext.Update()

        #x = self.cursorX
        #y = self.cursorY

        #if self._mouseEnabled and base.mouseWatcherNode.hasMouse():
        #    x += base.mouseWatcherNode.getMouseX()
        #    y += base.mouseWatcherNode.getMouseY()

        ## Translate absolute [-1,1] coordinates to pixels
        #x = base.win.getXSize() * (1 + x) / 2
        #y = base.win.getYSize() * (1 - y) / 2

        #self.System.injectMousePosition(x, y)

        #XXX: Kludge to fix librocket when shaders are enabled??
        OpenGL.GL.glActiveTexture(OpenGL.GL.GL_TEXTURE0)

        OpenGL.GL.glClearColor(1.0, 0.0, 0.0, 1.0)
        OpenGL.GL.glEnableClientState(OpenGL.GL.GL_VERTEX_ARRAY)
        OpenGL.GL.glEnableClientState(OpenGL.GL.GL_COLOR_ARRAY)

        OpenGL.GL.glEnable(OpenGL.GL.GL_BLEND)
        OpenGL.GL.glBlendFunc(OpenGL.GL.GL_SRC_ALPHA, OpenGL.GL.GL_ONE_MINUS_SRC_ALPHA)
        OpenGL.GL.glMatrixMode(OpenGL.GL.GL_PROJECTION)
        OpenGL.GL.glLoadIdentity()
        OpenGL.GL.glOrtho(0, self.win.getXSize(), self.win.getYSize(), 0, -100, 10000000)

        OpenGL.GL.glMatrixMode(OpenGL.GL.GL_MODELVIEW)
        OpenGL.GL.glLoadIdentity()

        self.rocketContext.Render()


app = MyApp()
app.run()
