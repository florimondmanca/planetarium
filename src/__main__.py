from .simulate import System

if __name__ == '__main__':
    s = System('planetfiles/earth_and_sun.planet')
    s.run(.001, 1000)
