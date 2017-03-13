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
    result = {'bodies': [], 'config': {}}
    for header in lines:  # will stop when finding an 'END' header or EOF
        header = header.capitalize()
        with get_creator(header) as creator:
            for line in lines:  # will stop when finding the next 'END'
                arg_name, value = parse_args(line)
                creator.set(arg_name, value)
        partial_result = creator.get()
        for key, func in partial_result.items():
            result[key] = func(result.get(key))
    return result


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
    """
    A Creator is a context manager.
    It is used to construct an object with certain arguments.
    Set its arguments inside a 'with' statement, then get the
    result of the construction with get().
    If an argument is left non-assigned after the construction, a
    ValueError will be raised.

    Usage
    -----
    with Creator() as creator:
        creator.set('foo', baz)
        creator.set('foo2', bush)
        ...
    result = creator.get()

    Subclass this base class to customize arguments.
    """

    def __init__(self):
        self.args = {}

    def __enter__(self):
        return self

    def set(self, arg_name, value):
        self.args[arg_name] = value

    def __exit__(self, *args):
        if any(value is None for value in self.args.values()):
            message = self._make_missing_message()
            raise ValueError(message)

    def _make_missing_message(self):
        return ''

    @property
    def missing_args(self):
        return (arg for arg in self.args if self.args[arg] is None)

    def get(self):
        return {}


class BodyCreator(Creator):
    """
    Result content
    --------------
    system_config : dict
    bodies : list of Body
    """
    body_cls = None

    def __init__(self):
        super().__init__()
        self.body = None
        self.args = {
            'name': None,
            'pos': None,
            'vel': None,
            'mass': None,
        }

    def __exit__(self, *args):
        super().__exit__(*args)
        self.body = self.body_cls(**self.args)

    def _make_missing_message(self):
        message = 'Following arguments are missing to create '
        message += self.body_cls.__name__ + ':'
        message += ' '.join(self.missing_args)
        return message

    def get(self):
        def func(bodies=None):
            if bodies is None:
                bodies = []
            bodies.append(self.body)
            return bodies
        return {'bodies': func}


class PlanetCreator(BodyCreator):
    body_cls = bodydefs.Planet


class StarCreator(BodyCreator):
    body_cls = bodydefs.Star


class SystemCreator(Creator):

    def __init__(self):
        super().__init__()
        self.config = {}
        self.args = {
            'dt': None,
            'method': None,
        }

    def __exit__(self, *args):
        super().__exit__(*args)
        for arg, val in self.args.items():
            self.config[arg] = val

    def _make_missing_message(self):
        message = 'Following arguments are missing to create System: '
        message += ' '.join(self.missing_args)
        return message

    def get(self):
        def func(config=None):
            if config is None:
                config = {}
            config.update(self.config)
            return config
        return {'config': func}


def get_creator(header):
    type_to_class = {
        'Planet': PlanetCreator,
        'Star': StarCreator,
        'System': SystemCreator,
    }
    try:
        return type_to_class[header]()
    except KeyError:
        raise SyntaxError('Unknown creator type: ' + str(header))
