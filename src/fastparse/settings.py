# Parser parameters

BUILDER_TYPES = {'System'}
BODY_TYPES = {'Planet', 'Star'}
HEADERS = set(t.upper() for t in BUILDER_TYPES.union(BODY_TYPES))
EOF = "END"


def MAKE_RESULTS_DICT():
    return {
        'bodies': [],
        'config': {},
    }
