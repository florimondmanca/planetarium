from .gui import Gui

if __name__ == '__main__':
    gui = Gui.from_file('planetfiles/five_planets.planet')
    gui.run()
