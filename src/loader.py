from . import bodydefs
from ast import literal_eval as make_tuple

ARG_TYPES = {
    'pos': make_tuple,
    'vel': make_tuple,
    'name': str,
    'mass': float,
    'dt': float,
    'method': str,
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
    lines = readfile(planetfilename)
    return load_from_lines_object(lines)


def load_from_lines_object(lines):
    system_config, bodies = {}, []
    for header in lines:  # will stop when finding an 'END' header or EOF
        header = header.capitalize()
        with get_creator(header)(system_config, bodies) as creator:
            for line in lines:  # will stop when finding the next 'END'
                arg_name, value = parse_args(line)
                creator.set(arg_name, value)
    return system_config, bodies


def parse_args(line):
    try:
        arg_name, value = line.split(':')
    except ValueError:
        info = ''
        if line in ('PLANET', 'STAR'):
            info += ' (a closing END statement may be missing)'
        else:
            info += ' (an argument declaration is probably mistyped)'
        raise SyntaxError('Could not parse line "{}"'.format(line) +
                          info)
    arg_name = arg_name.strip()
    value = value.strip()
    try:
        arg_type = ARG_TYPES[arg_name]
    except KeyError:
        raise TypeError('Unknown argument: ' + str(arg_name))
    return arg_name, arg_type(value)


class Creator:
    args = {}

    def __init__(self, system_config, bodies):
        self.system_config = system_config
        self.bodies = bodies

    def __enter__(self):
        return self

    def set(self, arg_name, value):
        self.args[arg_name] = value

    def __exit__(self):
        pass


class BodyCreator(Creator):
    body_cls = None
    args = {
        'name': None,
        'pos': None,
        'vel': None,
        'mass': None,
    }

    def __exit__(self, *args):
        if any(value is None for value in self.args.values()):
            missing = (arg for arg in self.args if self.args[arg] is None)
            message = 'Following arguments are missing to create '
            message += self.body_cls.__name__ + ':'
            message += ' '.join(missing)
            raise ValueError(message)
        body = self.body_cls(**self.args)
        self.bodies.append(body)


class PlanetCreator(BodyCreator):
    body_cls = bodydefs.Planet


class StarCreator(BodyCreator):
    body_cls = bodydefs.Star


class SystemCreator(Creator):
    args = {
        'dt': None,
        'method': None,
    }

    def __exit__(self, *args):
        if any(value is None for value in self.args.values()):
            missing = (arg for arg in self.args if self.args[arg] is None)
            message = 'Following arguments are missing to configure System: '
            message += ' '.join(missing)
            raise ValueError(message)
        for arg, val in self.args:
            self.system_config[arg] = val


def get_creator(header):
    type_to_class = {
        'Planet': PlanetCreator,
        'Star': StarCreator,
        'System': SystemCreator,
    }
    try:
        return type_to_class[header]
    except KeyError:
        raise SyntaxError('Unknown creator type: ' + str(header))
