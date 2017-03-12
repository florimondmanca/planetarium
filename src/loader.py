from . import bodydefs
from ast import literal_eval as make_tuple


class Loader:
    known_types = {
        'int': int,
        'str': str,
        'float': float,
        'tuple': make_tuple,
    }

    def readfile(planetfilename):
        lines = []
        with open(planetfilename) as f:
            for line in f:
                lines.append(line.strip())
        lines.reverse()  # make it a FIFO queue
        return lines

    def load(planetfilename):
        bodies = []
        lines = Loader.readfile(planetfilename)
        while lines:
            header = lines.pop()
            body_type = header.capitalize()
            with Creator.get(body_type)(bodies) as creator:
                line = header
                while line != "END":
                    line = lines.pop()
                    arg_name, value = Loader.parse_args(line)
                    creator.set(arg_name, value)
        return bodies

    def parse_args(line):
        arg_name, arg_type, value = line.split(':')
        arg_name = arg_name.strip()
        arg_type = arg_type.strip()
        value = value.strip()
        value = Loader.known_types[arg_type](value)
        return arg_name, value


class Creator:
    body_cls = None

    def __init__(self, bodies):
        self.bodies = bodies
        self.args = {
            'name': None,
            'pos': None,
            'vel': None,
            'mass': None,
        }

    def __enter__(self):
        return self

    def set(self, arg_name, value):
        self.args[arg_name] = value

    def __exit__(self, *args):
        if any(value is None for value in self.args.values()):
            missing = (arg for arg in self.args if self.args[arg] is None)
            message = self.body_cls.__name__
            message += ' misses the following arguments: '
            message += ' '.join(missing)
            raise ImportError(message)
        self.bodies.append(self.body_cls(**self.args))


class PlanetCreator(Creator):
    body_cls = bodydefs.Planet


def get_creator(body_type):
    type_to_class = {
        'Planet': PlanetCreator,
    }
    return type_to_class[body_type]


Creator.get = get_creator
