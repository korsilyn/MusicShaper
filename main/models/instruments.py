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


MusicInstrument.define('PluckSynth', {
    'attackNoise': FloatSettingValue(initial=1, min_v=0.1, max_v=20),
    'dampening': FloatSettingValue(initial=4000, min_v=0, step=100),
    'resonance': FloatSettingValue(initial=0.7, min_v=0, max_v=0.99),
})


MusicInstrument.define('FMSynth', {
    'harmonicity': FloatSettingValue(initial=3, min_v=0),
    'detune': FloatSettingValue(initial=0, step=100),
    'oscillator': {
        'type': ChoiceSettingValue(
            initial='sine',
            choices=['sine', 'square', 'triangle', 'sawtooth']
        )
    },
    'envelope': {
        'attack':  FloatSettingValue(initial=0.01, min_v=0),
        'decay':   FloatSettingValue(initial=0.01, min_v=0),
        'sustain': FloatSettingValue(initial=1, min_v=0, max_v=1),
        'release': FloatSettingValue(initial=0.5, min_v=0.01),
    },
    'modulation': {
        'type': ChoiceSettingValue(
            initial='square',
            choices=['sine', 'square', 'triangle', 'sawtooth']
        )
    },
    'modulationEnvelope': {
        'attack':  FloatSettingValue(initial=0.5, min_v=0),
        'decay':   FloatSettingValue(initial=0, min_v=0),
        'sustain': FloatSettingValue(initial=1, min_v=0, max_v=1),
        'release': FloatSettingValue(initial=0.5, min_v=0.01),
    }
})


MusicInstrument.define('MonoSynth', {
    'frequency': FloatSettingValue(initial=261, min_v=0, step=100),
    'detune': FloatSettingValue(initial=0, step=10),
    'oscillator': {
        'type': ChoiceSettingValue(
            initial='sine',
            choices=['sine', 'square', 'triangle', 'sawtooth']
        )
    },
    'filter': {
        'Q': FloatSettingValue(initial=6, min_v=0),
        'type': ChoiceSettingValue(
            initial='lowpass',
            choices=[
                "lowpass", "highpass", "bandpass",
                "lowshelf", "highshelf", "notch",
                "allpass", "peaking",
            ]
        ),
        'rolloff': ChoiceSettingValue(
            initial=-24,
            choices=[-12, -24, -48, -96]
        )
    },
    'envelope': {
        'attack':  FloatSettingValue(initial=0.005, min_v=0),
        'decay':   FloatSettingValue(initial=0.1, min_v=0),
        'sustain': FloatSettingValue(initial=0.9, min_v=0, max_v=1),
        'release': FloatSettingValue(initial=1, min_v=0.01),
    },
    'filterEnvelope': {
        'attack':  FloatSettingValue(initial=0.06, min_v=0),
        'decay':   FloatSettingValue(initial=0.2, min_v=0),
        'sustain': FloatSettingValue(initial=0.5, min_v=0, max_v=1),
        'release': FloatSettingValue(initial=2, min_v=0.01),
        'baseFrequency': FloatSettingValue(initial=200, min_v=0, step=100),
        'octaves': FloatSettingValue(initial=7, min_v=0),
        'exponent': FloatSettingValue(initial=2),
    },
})


MusicInstrument.define('DuoSynth', {
    'vibratoAmount': FloatSettingValue(initial=0.5, min_v=0),
    'vibratoRate': FloatSettingValue(initial=5, min_v=0, step=10),
    'harmonicity': FloatSettingValue(initial=1.5, min_v=0),
    'voice0': {
        'volume': FloatSettingValue(initial=-20, min_v=-50, max_v=50),
        'portamento': FloatSettingValue(initial=0, min_v=0),
        'oscillator': {
            'type': ChoiceSettingValue(
                initial='sine',
                choices=['sine', 'square', 'triangle', 'sawtooth']
            )
        },
        'filterEnvelope': {
            'attack':  FloatSettingValue(initial=0.01, min_v=0),
            'decay':   FloatSettingValue(initial=0, min_v=0),
            'sustain': FloatSettingValue(initial=1, min_v=0, max_v=1),
            'release': FloatSettingValue(initial=0.5, min_v=0.01),
        },
        'envelope': {
            'attack':  FloatSettingValue(initial=0.01, min_v=0),
            'decay':   FloatSettingValue(initial=0, min_v=0),
            'sustain': FloatSettingValue(initial=1, min_v=0, max_v=1),
            'release': FloatSettingValue(initial=0.5, min_v=0.01),
        },
    },
    'voice1': {
        'volume': FloatSettingValue(initial=-20, min_v=-50, max_v=50),
        'portamento': FloatSettingValue(initial=0, min_v=0),
        'oscillator': {
            'type': ChoiceSettingValue(
                initial='sine',
                choices=['sine', 'square', 'triangle', 'sawtooth']
            )
        },
        'filterEnvelope': {
            'attack':  FloatSettingValue(initial=0.01, min_v=0),
            'decay':   FloatSettingValue(initial=0, min_v=0),
            'sustain': FloatSettingValue(initial=1, min_v=0, max_v=1),
            'release': FloatSettingValue(initial=0.5, min_v=0.01),
        },
        'envelope': {
            'attack':  FloatSettingValue(initial=0.01, min_v=0),
            'decay':   FloatSettingValue(initial=0, min_v=0),
            'sustain': FloatSettingValue(initial=1, min_v=0, max_v=1),
            'release': FloatSettingValue(initial=0.5, min_v=0.01),
        },
    }
})
