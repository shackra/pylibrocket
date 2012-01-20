import sf

import pyrokit
import pyrokit.sfml


def main():
    window = sf.RenderWindow(sf.VideoMode(640, 480), 'Drawing an image with SFML')
    window.framerate_limit = 60

    #texture = sf.Texture.load_from_file('python-logo.png')
    #sprite = sf.Sprite(texture)

    shape0 = sf.Shape()
    map(shape0.add_point, *zip(
            (0.0, 50.0),
            (50.0, 200.0),
            (50.0, 50.0),
            (25.0, 0.0),
            ))

    shape0.position = (300, 200)
    shape0.color = sf.Color(50, 100, 200, 128)
    shape0.origin = (25.0, 32.0)

    pyrokit.sfml.initializeSystem()
    pyrokit.sfml.initializeRenderer(window)
    pyrokit.manager.finishInitialization()

    running = True
    while running:
        for event in window.iter_events():
            # Stop running if the application is closed
            # or if the user presses Escape
            if (event.type == sf.Event.CLOSED or
                (event.type == sf.Event.KEY_PRESSED and event.code == sf.Keyboard.ESCAPE)):
                running = False

        shape0.rotate(1)

        window.clear(sf.Color.BLACK)

        #window.draw(sprite)
        window.draw(shape0)

        pyrokit.manager.render()

        window.display()

    window.close()


if __name__ == '__main__':
    main()
