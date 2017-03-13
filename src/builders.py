from . import bodydefs


class Builder:
    """
    A Builder is a context manager.
    It is used to construct an object with certain arguments.
    Set its arguments inside a 'with' statement, then build the
    result of the construction with build().
    The builder's result is a mapping (name of data bunch -> function
    to access or update it).
    If an argument is left non-assigned after the construction, a
    ValueError will be raised.

    Example usage
    -----
    with Builder() as builder:
        builder.gather('foo', baz)
        builder.gather('foo2', bush)
        ...
    result = builder.build()
    bodies = result['bodies']

    When subclassing Builder:
        You must:
        - override _build(result) to define how the child Builder should build
        its data into a result dictionnary (not doing so results in a
        NotImplementedError being raised at call time)
        You can:
        - override __exit__() - be sure to call super()
        - override _make_missing_message()

    """

    def __init__(self, *args):
        self.args = {arg: None for arg in args}

    def __enter__(self):
        return self

    def gather(self, arg_name, value):
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

    def _build(self, result):
        raise NotImplementedError

    def build(self, result=None):
        """
        Builds the arguments the Builder gathered into a dictionnary.

        Parameters
        ----------
        result : dict (optional)
            If passed the builder will update it instead of
            creating a new one.
        """
        if result is None:
            result = {}
        return self._build(result)


class BodyBuilder(Builder):
    body_cls = None

    def __init__(self):
        super().__init__('name', 'pos', 'vel', 'mass')
        self.body = None

    def __exit__(self, *args):
        super().__exit__(*args)
        self.body = self.body_cls(**self.args)

    def _make_missing_message(self):
        message = 'Following arguments are missing to create '
        message += self.body_cls.__name__ + ':'
        message += ' '.join(self.missing_args)
        return message

    def _build(self, result):
        bodies = result.get('bodies', [])
        bodies.append(self.body)
        result['bodies'] = bodies
        return result


class PlanetBuilder(BodyBuilder):
    body_cls = bodydefs.Planet


class StarBuilder(BodyBuilder):
    body_cls = bodydefs.Star


class SystemBuilder(Builder):

    def __init__(self):
        super().__init__('dt', 'method')
        self.config = {}

    def __exit__(self, *args):
        super().__exit__(*args)
        for arg, val in self.args.items():
            self.config[arg] = val

    def _make_missing_message(self):
        message = 'Following arguments are missing to create System: '
        message += ' '.join(self.missing_args)
        return message

    def _build(self, result):
        config = result.get('config', {})
        config.update(self.config)
        result['config'] = config
        return result


def get_builder(header):
    type_to_class = {
        'Planet': PlanetBuilder,
        'Star': StarBuilder,
        'System': SystemBuilder,
    }
    try:
        return type_to_class[header]()
    except KeyError:
        raise SyntaxError('Unknown builder type: ' + str(header))
