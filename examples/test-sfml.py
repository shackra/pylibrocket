import os

import sfml

import pylibrocket
import pylibrocket.sf
import pylibrocket.opengl

import rocket


def main():
    window = sfml.RenderWindow(sfml.VideoMode(640, 480),
                               'Pylibrocket & Python-SFML')
    window.framerate_limit = 60
    
    pylibrocket.sf.initializeSystem()
    #pylibrocket.sfml.initializeRenderer(window)
    pylibrocket.opengl.initializeRenderer()
    pylibrocket.manager.finishInitialization()
    
    rocketContext = rocket.CreateContext('main',
                                         rocket.Vector2i(
            window.size.x, window.size.y))
    
    #os.chdir(os.path.dirname(__file__))
    rocket.LoadFontFace("template/data/assets/Delicious-Roman.otf")
    rocket.LoadFontFace("template/data/assets/Delicious-Bold.otf")
    rocket.LoadFontFace("template/data/assets/Delicious-BoldItalic.otf")
    rocket.LoadFontFace("template/data/assets/Delicious-Italic.otf")
    rocketContext.LoadDocument('template/data/tutorial.rml').Show()
    
    running = True
    while running:
        for event in window.events:
            # Stop running if the application is closed
            # or if the user presses Escape
            if type(event) == sfml.CloseEvent or \
            (type(event) == sfml.KeyEvent and 
             event.code == sfml.Keyboard.ESCAPE):
                running = False
            else:
                pylibrocket.sf.processEvent(rocketContext, event)
        
        window.clear(sfml.Color.BLACK)
        
        #window.draw(sprite)
        pylibrocket.manager.render(None)
        
        window.display()
    window.close()
    
if __name__ == '__main__':
    main()
    
