from .simulate import System

if __name__ == '__main__':
    s = System.from_file('planetfiles/earth_and_sun.planet')
    s.run(.00001, 1000)
