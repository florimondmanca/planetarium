# Body parameters
STATE_QUEUE_LENGTH = 3  # max number of states a Body can remember

#
STATE_DTYPE = [
    ('pos', 'f', 2),
    ('vel', 'f', 2),
    ('acc', 'f', 2),
    ('mass', 'f'),
]
