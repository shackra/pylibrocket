"""Initialize SFML integration.

"""
import pyrokit


cdef extern from "SFML/Window/WindowHandle.hpp" namespace "sf":
    ctypedef void* WindowHandle

cdef extern from "SFML/Graphics.hpp" namespace "sf":
    cdef cppclass RenderTarget

    cdef cppclass RenderWindow:
        RenderWindow(WindowHandle handle)
        WindowHandle GetSystemHandle()

######### 
#XXX: HORRIBLE HACK -.-
# This should really be done by either exposing p_this to Python in pysfml2, sharing the RenderTarget type in an
# installed .pxd, or some other workaround. Also, this hack doesn't actually work. No energy to debug it at the moment.
cdef class _RenderTarget:
    cdef RenderTarget *p_this

cdef class _RenderWindow(_RenderTarget):
    pass
######### 

cdef extern from "Rocket/Core.h" namespace "Rocket::Core":
    cdef void SetRenderInterface(RenderInterface*)
    cdef cppclass RenderInterface

cdef extern from "SystemInterfaceSFML.h":
    cdef cppclass RocketSFMLSystemInterface:
        RocketSFMLSystemInterface()

cdef extern from "RenderInterfaceSFML.h":
    cdef cppclass RocketSFMLRenderer:
        RocketSFMLRenderer()
        void SetWindow(RenderWindow*)
        RenderWindow* GetWindow()
        void Resize()


cdef RocketSFMLSystemInterface* systemInterface

cpdef initializeSystem():
    global systemInterface
    systemInterface = new RocketSFMLSystemInterface()


cdef RocketSFMLRenderer* renderer

cpdef initializeRenderer(window):
    global renderer
    renderer = new RocketSFMLRenderer()
    renderer.SetWindow(<RenderWindow*> (<_RenderWindow> window).p_this)
