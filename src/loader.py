from .builders import get_builder
from . import settings
from ast import literal_eval as make_tuple

ARG_TYPES = {
    'pos': make_tuple,
    'vel': make_tuple,
    'name': str,
    'mass': float,
    'dt': float,
    'method': str,
}


class Lines:
    """
    Iterator that allows easier management of .planet files
    A for loop on this iterator will stop every time an 'END' statement
    is encountered in the .planet files

    Consider the following .planet file:
        PLANET              (A)
            name: Earth     |
            pos: (1, 0)     | (2)
            vel: (0, .5)    |
            mass: 3e-5      |
        END

        STAR                (C)
            name: Sun       |
            pos: (0, 0)     | (2)
            vel: (0, 0)     |
            mass: 1         |
        END

    and the following code snippet:

    for line in lines:  # prints line (A) at first iteration, (B) at second
        print(line)
        for inner in lines:  # prints (1) at first iteration, (2) at second
            print(inner)

    """

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
            if line == settings.EOF:
                raise StopIteration
            while not line:
                line = next(self)
            return line


def readfile(planetfilename):
    lines = []
    with open(planetfilename) as f:
        for line in f:
            lines.append(line.strip())
    lines.reverse()  # makes it a FIFO queue
    return Lines(lines)


def parse_arg_and_value(line):
    try:
        arg_name, value = line.split(':')
        return arg_name.strip(), value.strip()
    except ValueError:
        info = ''
        if line in settings.HEADERS:
            info += (' (a closing {} statement may be missing)'
                     .format(settings.EOF))
        else:
            info += ' (an argument declaration is probably mistyped)'
        raise SyntaxError('Could not parse line "{}"'.format(line) +
                          info)


def get_arg_type(arg_name):
    try:
        return ARG_TYPES[arg_name]
    except KeyError:
        raise TypeError('Unknown argument: ' + str(arg_name))


def parse_args(line):
    arg_name, value = parse_arg_and_value(line)
    arg_type = get_arg_type(arg_name)
    return arg_name, arg_type(value)


def load_from_lines_object(lines):
    result = settings.MAKE_RESULTS_DICT()
    for header in lines:
        header = header.capitalize()
        with get_builder(header) as builder:
            for line in lines:
                arg_name, value = parse_args(line)
                builder.gather(arg_name, value)
        result = builder.build(result)
    return result


def load(planetfilename):
    """
    Parameters
    ----------
    planetfilename : str
        Name of a .planet file

    Returns
    -------
    result : dict
        A mapping of the .planet file data:
        'bodies' : a list of the constructed Body objects
        'config': configuration data for the simulation System
    """
    lines = readfile(planetfilename)
    return load_from_lines_object(lines)
