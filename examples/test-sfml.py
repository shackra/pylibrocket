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
    rocket.LoadFontFace("data/assets/Delicious-Roman.otf")
    rocket.LoadFontFace("data/assets/Delicious-Bold.otf")
    rocket.LoadFontFace("data/assets/Delicious-BoldItalic.otf")
    rocket.LoadFontFace("data/assets/Delicious-Italic.otf")
    rocketContext.LoadDocument('data/tutorial.rml').Show()
    
    running = True
    while running:
        for event in window.events:
            # Stop running if the application is closed
            # or if the user presses Escape
            if type(event) == sfml.CloseEvent:
                running = False

            elif type(event) == sfml.KeyEvent:
                if event.code == sfml.Keyboard.F5:
                    # refresh the document
                    # HOW?
                    pass
                elif event.code == sfml.Keyboard.ESCAPE:
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
    
