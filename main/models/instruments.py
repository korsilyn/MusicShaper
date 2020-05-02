from .project import MusicInstrument
from .settings import FloatSettingValue, ChoiceSettingValue
from math import inf


MusicInstrument.define('Synth', {
    'oscillator': {
        'type': ChoiceSettingValue(
            initial='sine',
            choices=['sine', 'square', 'triangle', 'sawtooth']
        )
    },
    'envelope': {
        'attack':  FloatSettingValue(initial=0.005, min=0),
        'decay':   FloatSettingValue(initial=0.1,   min=0),
        'sustain': FloatSettingValue(initial=0.3,   min=0, max=1),
        'release': FloatSettingValue(initial=1,     min=0.01),
    }
})


MusicInstrument.define('NoiseSynth', {
    'noise': {
        'type': ChoiceSettingValue(
            initial='white',
            choices=['white', 'brown', 'pink']
        )
    },
    'envelope': {
        'attack':  FloatSettingValue(initial=0.005, min=0),
        'decay':   FloatSettingValue(initial=0.1, min=0),
        'sustain': FloatSettingValue(initial=0, min=0, max=1),
    }
})


MusicInstrument.define('AMSynth', {
    'harmonicity': FloatSettingValue(initial=3, min=0),
    'detune':      FloatSettingValue(initial=0, step=100),
    'oscillator': {
        'type': ChoiceSettingValue(
            initial='sine',
            choices=['sine', 'square', 'triangle', 'sawtooth']
        )
    },
    'modulation': {
        'type': ChoiceSettingValue(
            initial='square',
            choices=['square', 'sine', 'triangle', 'sawtooth']
        )
    },
    'envelope': {
        'attack':  FloatSettingValue(initial=0.01, min=0),
        'decay':   FloatSettingValue(initial=0.01, min=0),
        'sustain': FloatSettingValue(initial=1,    min=0, max=1),
        'release': FloatSettingValue(initial=0.5,  min=0.01),
    },
    'modulationEnvelope': {
        'attack':  FloatSettingValue(initial=0.5, min=0),
        'decay':   FloatSettingValue(initial=0.0, min=0),
        'sustain': FloatSettingValue(initial=1,   min=0, max=1),
        'release': FloatSettingValue(initial=0.5, min=0.01),
    }
})
