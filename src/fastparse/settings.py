from ..core.settings import STATE_DTYPE
import numpy as np

# Parser parameters

BUILDER_TYPES = {'System'}
BODY_TYPES = {'Planet', 'Star'}
HEADERS = set(t.upper() for t in BUILDER_TYPES.union(BODY_TYPES))
EOF = "END"


def MAKE_RESULTS_DICT():
    return {
        'bodynames': np.zeros((1,), dtype=STATE_DTYPE),
        'first_state': [],
        'config': {},
    }
