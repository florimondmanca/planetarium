# Parser parameters

BUILDER_TYPES = {'System'}
BODY_TYPES = {'Planet', 'Star'}
HEADERS = set(t.upper() for t in BUILDER_TYPES.union(BODY_TYPES))
EOB = "END"  # end of block


def MAKE_RESULTS_DICT():
    return {
        'names': [],
        'state': None,
        'config': {},
    }
