from .gui import Gui

if __name__ == '__main__':
    gui = Gui.from_file('planetfiles/twins.planet')
    gui.run()
