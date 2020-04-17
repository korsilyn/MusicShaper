from .project import MusicInstrument
from math import inf


MusicInstrument.define('Synth', {
    'oscillator': {
        'type': ('sine', 'square', 'triangle', 'sawtooth')
    },
    'envelope': {
        'attack':  (0.005, 0),
        'decay':   (0.1, 0),
        'sustain': (0.3, 0, 1),
        'release': (1, 0.01),
    }
})


MusicInstrument.define('NoiseSynth', {
    'noise': {
        'type': ('white', 'brown', 'pink')
    },
    'envelope': {
        'attack':  (0.005, 0),
        'decay':   (0.1, 0),
        'sustain': (0, 0, 1),
    }
})


MusicInstrument.define('AMSynth', {
    'harmonicity': (3, 0),
    'detune': (0, -inf, inf, 100),
    'oscillator': {
        'type': ('sine', 'square', 'triangle', 'sawtooth')
    },
    'modulation': {
        'type': ('square', 'sine', 'triangle', 'sawtooth')
    },
    'envelope': {
        'attack':  (0.01, 0),
        'decay':   (0.01, 0),
        'sustain': (1, 0, 1),
        'release': (0.5, 0.01),
    },
    'modulationEnvelope': {
        'attack':  (0.5, 0),
        'decay':   (0.0, 0),
        'sustain': (1, 0, 1),
        'release': (0.5, 0.01),
    }
})
