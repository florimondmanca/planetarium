from . import bodydefs
from ast import literal_eval as make_tuple

ARG_TYPES = {
    'pos': make_tuple,
    'vel': make_tuple,
    'name': str,
    'mass': float,
}


def readfile(planetfilename):
    lines = []
    with open(planetfilename) as f:
        for line in f:
            lines.append(line.strip())
    lines.reverse()  # make it a FIFO queue
    return Lines(lines)


class Lines:

    def __init__(self, lines):
        self.lines = lines

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.lines)

    def __next__(self):
        if not self.lines:
            raise StopIteration
        else:
            line = self.lines.pop()
            if line == "END":
                raise StopIteration
            while not line:
                line = next(self)
            return line


def load(planetfilename):
    bodies = []
    lines = readfile(planetfilename)
    for header in lines:
        body_type = header.capitalize()
        with Creator.get(body_type)(bodies) as creator:
            for line in lines:
                arg_name, value = parse_args(line)
                creator.set(arg_name, value)
    return bodies


def parse_args(line):
    try:
        arg_name, value = line.split(':')
    except ValueError:
        raise ValueError('Could not parse line {}'.format(line))
    arg_name = arg_name.strip()
    value = value.strip()
    try:
        arg_type = ARG_TYPES[arg_name]
    except KeyError:
        raise KeyError('Unknown parameter for body creation ' + arg_name)
    return arg_name, arg_type(value)


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
