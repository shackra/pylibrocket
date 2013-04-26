# coding: utf-8
"""Initialize SFML integration.
"""
from libcpp cimport bool

import sfml
import pylibrocket


cdef extern from "SFML/Window/WindowHandle.hpp" namespace "sf":
    ctypedef void* WindowHandle
    
cdef extern from "SFML/Graphics.hpp" namespace "sf":
    cdef cppclass RenderTarget
    
    cdef cppclass Window:
        pass

    cdef cppclass RenderWindow(Window):
        RenderWindow(WindowHandle handle)
        WindowHandle GetSystemHandle()
        
cdef extern from "SFML/Window/Keyboard.hpp" namespace "sf::Keyboard":
    enum Key:
        pass

######### 
#XXX: HORRIBLE HACK -.-
# This should really be done by either exposing p_this to Python in pysfml2, sharing the RenderTarget type in an
# installed .pxd, or some other workaround. Also, this hack doesn't actually work. No energy to debug it at the moment.
cdef class _RenderTarget:
    cdef RenderTarget *p_this
    
cdef class _RenderWindow(_RenderTarget):
    pass
######### 

cdef extern from "Rocket/Core/Input.h" namespace "Rocket::Core::Input":
    enum KeyIdentifier:
        pass

cdef extern from "Rocket/Core.h" namespace "Rocket::Core":
    cdef cppclass SystemInterface
    cdef void SetSystemInterface(SystemInterface*)
    cdef cppclass RenderInterface
    cdef void SetRenderInterface(RenderInterface*)
    
    cdef cppclass StringBase[T]:
        StringBase(T*)
        
    cdef cppclass Context:
        bool ProcessKeyDown(KeyIdentifier, int)
        bool ProcessKeyUp(KeyIdentifier, int)
        bool ProcessTextInput(StringBase[char])
        void ProcessMouseMove(int, int, int)
        void ProcessMouseButtonDown(int, int)
        void ProcessMouseButtonUp(int, int)
        bool ProcessMouseWheel(int, int)
        
    cdef Context* GetContext(StringBase[char])
    
cdef extern from "SystemInterfaceSFML.h":
    cdef cppclass RocketSFMLSystemInterface:
        RocketSFMLSystemInterface()
        KeyIdentifier TranslateKey(Key)
        int GetKeyModifiers()
        
cdef extern from "RenderInterfaceSFML.h":
    cdef cppclass RocketSFMLRenderer:
        RocketSFMLRenderer()
        void SetWindow(RenderWindow*)
        RenderWindow* GetWindow()
        void Resize()
        
        
cdef RocketSFMLSystemInterface* systemInterface = NULL

cpdef initializeSystem():
    global systemInterface
    systemInterface = new RocketSFMLSystemInterface()
    SetSystemInterface(<SystemInterface*> systemInterface)
    
    
cdef RocketSFMLRenderer* renderer

cpdef initializeRenderer(window):
    global renderer
    renderer = new RocketSFMLRenderer()
    renderer.SetWindow(<RenderWindow*> (<_RenderWindow> window).p_this)
    SetRenderInterface(<RenderInterface*> renderer)
    
    
def processEvent(context, event):
    if type(event) is sfml.window.ResizeEvent and renderer != NULL:
        renderer.Resize()
        
    elif type(event) is sfml.window.MouseMoveEvent:
        processMouseMove(context, event)
        
    elif type(event) is sfml.window.MouseButtonEvent:
        if event.pressed:
            processMouseButtonPressed(context, event)
            
        if event.released:
            processMouseButtonReleased(context, event)
            
    elif type(event) is sfml.window.MouseWheelEvent:
        processMouseWheelMoved(context, event)
        
    elif type(event) is sfml.window.TextEvent:
        processTextEntered(context, event)
        
    elif type(event) is sfml.window.KeyEvent:
        if event.pressed:
            processKeyPressed(context, event)
            
        if event.released:
            processKeyReleased(context, event)
            
cdef Context* cppContextFromPy(pyCtx):
    cdef StringBase[char]* name = new StringBase[char](<char*> pyCtx.name)
    cdef Context* context = GetContext(name[0])
    del name
    return context

def processMouseMove(context, event):
    cppContextFromPy(context).ProcessMouseMove(
        event.position.x,
        event.position.y,
        systemInterface.GetKeyModifiers())
    
def processMouseButtonPressed(context, event):
    cppContextFromPy(context).ProcessMouseButtonDown(
        event.button,
        systemInterface.GetKeyModifiers())
    
def processMouseButtonReleased(context, event):
    cppContextFromPy(context).ProcessMouseButtonUp(
        event.button,
        systemInterface.GetKeyModifiers())
    
    
def processMouseWheelMoved(context, event):
    cppContextFromPy(context).ProcessMouseWheel(
        event.delta,
        systemInterface.GetKeyModifiers())
    
def processTextEntered(context, event):
    unicodechr = chr(event.unicode)
    cdef StringBase[char]* text = new StringBase[char](<char*> unicodechr)
    cppContextFromPy(context).ProcessTextInput(text[0])
    del text
    del unicodechr
    
def processKeyPressed(context, event):
    cppContextFromPy(context).ProcessKeyDown(systemInterface.TranslateKey(
            event.code), systemInterface.GetKeyModifiers())
    
def processKeyReleased(context, event):
    #if event.Key.Code == sfml.Key.F8:
    #    Rocket.Debugger.SetVisible(!Rocket.Debugger.IsVisible())
    
    cppContextFromPy(context).ProcessKeyUp(systemInterface.TranslateKey(
            event.code), systemInterface.GetKeyModifiers())

def debugger():
    """ Turn libRocket debugging On or Off.
    """
    Rocket.Debugger.SetVisible(not Rocket.Debugger.IsVisible())
