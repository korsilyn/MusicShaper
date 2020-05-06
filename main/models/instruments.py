'''
Модуль объявления настроек музыкальных инструментов
'''

from .project import MusicInstrument
from .settings import FloatSettingValue, ChoiceSettingValue


MusicInstrument.define('Synth', {
    'oscillator': {
        'type': ChoiceSettingValue(
            initial='sine',
            choices=['sine', 'square', 'triangle', 'sawtooth']
        )
    },
    'envelope': {
        'attack':  FloatSettingValue(initial=0.005, min_v=0),
        'decay':   FloatSettingValue(initial=0.1, min_v=0),
        'sustain': FloatSettingValue(initial=0.3, min_v=0, max_v=1),
        'release': FloatSettingValue(initial=1, min_v=0.01),
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
        'attack':  FloatSettingValue(initial=0.005, min_v=0),
        'decay':   FloatSettingValue(initial=0.1, min_v=0),
        'sustain': FloatSettingValue(initial=0, min_v=0, max_v=1),
    }
})


MusicInstrument.define('AMSynth', {
    'harmonicity': FloatSettingValue(initial=3, min_v=0),
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
        'attack':  FloatSettingValue(initial=0.01, min_v=0),
        'decay':   FloatSettingValue(initial=0.01, min_v=0),
        'sustain': FloatSettingValue(initial=1, min_v=0, max_v=1),
        'release': FloatSettingValue(initial=0.5, min_v=0.01),
    },
    'modulationEnvelope': {
        'attack':  FloatSettingValue(initial=0.5, min_v=0),
        'decay':   FloatSettingValue(initial=0.0, min_v=0),
        'sustain': FloatSettingValue(initial=1, min_v=0, max_v=1),
        'release': FloatSettingValue(initial=0.5, min_v=0.01),
    }
})
