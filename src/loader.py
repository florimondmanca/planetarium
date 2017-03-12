import bodydef


class Loader:
    known_types = {
        'int': int,
        'str': str,
        'float': float,
        'tuple': tuple,
    }

    def load(planetfilename):
        bodies = []
        with open(planetfilename) as f:
            header = f.readline().strip()
            body_type = header.capitalize()
            with Creator.get(body_type)(bodies) as creator:
                line = header
                while line != "END":
                    line = f.readline().strip()
                    arg_name, value = Loader.parse_args(line)
                    creator.set(arg_name, value)
        return bodies

    def parse_args(line):
        arg_name, arg_type, value = line.split(':')
        value = Loader.known_types[arg_type](value)
        return arg_name, value


class Creator:
    body_cls = None

    def __init__(self, bodies):
        self.bodies = bodies
        self.args = {
            'name': None,
            'pos0': None,
            'vel0': None,
            'mass': None,
        }

    def __enter__(self):
        return self

    def set(self, arg_name, value):
        self.args[arg_name] = value

    def __exit__(self):
        if any(value is None for value in self.args.values()):
            missing = (arg for arg in self.args if self.args[arg] is None)
            message = self.body_cls.__name__
            message += ' misses the followinf arguments: '
            message += ' '.join(missing)
            raise ImportError(message)
        self.bodies.append(self.body_cls(*self.args))


class PlanetCreator(Creator):
    body_cls = bodydef.Planet


def get_creator(body_type):
    type_to_class = {
        'Planet': PlanetCreator,
    }
    return type_to_class[body_type]


Creator.get = get_creator
