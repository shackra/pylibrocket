import os

import sfml

import pylibrocket
import pylibrocket.sfml
import pylibrocket.opengl

import rocket


def main():
    window = sfml.RenderWindow(sfml.VideoMode(640, 480), 'Drawing an image with SFML')
    window.framerate_limit = 60
    
    #texture = sfml.Texture.load_from_file('python-logo.png')
    #sprite = sfml.Sprite(texture)
    
    shape0 = sfml.Shape()
    map(shape0.add_point, *zip(
            (0.0, 50.0),
            (50.0, 200.0),
            (50.0, 50.0),
            (25.0, 0.0),
            ))
    
    shape0.position = (300, 200)
    shape0.color = sfml.Color(50, 100, 200, 128)
    shape0.origin = (25.0, 32.0)
    
    pylibrocket.sfml.initializeSystem()
    #pylibrocket.sfml.initializeRenderer(window)
    pylibrocket.opengl.initializeRenderer()
    pylibrocket.manager.finishInitialization()
    
    rocketContext = rocket.CreateContext('main', rocket.Vector2i(window.width, window.height))
    
    os.chdir(os.path.dirname(__file__))
    rocket.LoadFontFace("data/Delicious-Roman.otf")
    rocket.LoadFontFace("data/Delicious-Bold.otf")
    rocket.LoadFontFace("data/Delicious-BoldItalic.otf")
    rocket.LoadFontFace("data/Delicious-Italic.otf")
    
    rocketContext.LoadDocument('data/demo.rml').Show()
    
    running = True
    while running:
        for event in window.events:
            # Stop running if the application is closed
            # or if the user presses Escape
            if (event.type == sfml.Event.CloseEvent or
                (event.type == sfml.Event.KeyEvent and event.code == sfml.Keyboard.ESCAPE)):
                running = False
                
            else:
                pylibrocket.sfml.processEvent(rocketContext, event)
                
        shape0.rotate(1)
        
        window.clear(sfml.Color.BLACK)
        
        #window.draw(sprite)
        window.draw(shape0)
        
        pylibrocket.manager.render(None)
        
        window.display()
        
    window.close()
    
    
if __name__ == '__main__':
    main()
    
