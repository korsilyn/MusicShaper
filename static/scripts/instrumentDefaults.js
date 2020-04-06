function undefinedOr(v, d) {
    return v === undefined ? d : v;
}

function Positive(dv = 0, step = 0.1) {
    return [dv, 0, Infinity, step];
}

function RealNumber(dv = 0, step = 0.1) {
    return [dv, -Infinity, Infinity, step];
}

function Frequency(dv = 261) {
    return Positive(dv, 16);
}

function Detune(dv = 0) {
    return [dv, -Infinity, Infinity, 100];
}

function Decibel(dv = -10) {
    return [dv, -Infinity, Infinity, 0.5];
}

function defaultEnvelope({ attack = 0.005, decay = 0.1, sustain = 0.3, release = 1 } = {}, remove = []) {
    let env = {
        attack:  [attack,     0],
        decay:   [decay,      0],
        sustain: [sustain, 0, 1],
        release: [release, 0.01],
    };
    remove.forEach(rkey => delete env[rkey]);
    return env;
}

function filterEnvelope(values = {}, remove = []) {
    let env = defaultEnvelope(values);
    env = {
        ...env,
        baseFrequency: Frequency(undefinedOr(values.baseFrequency, 200)),
        octaves: Positive(undefinedOr(values.octaves, 7)),
        exponent: RealNumber(undefinedOr(values.exponent, 1), 1),
    }
    remove.forEach(rkey => delete env[rkey]);
    return env;
}

function defaultOscillator(defaultType) {
    const types = ['sine', 'square', 'triangle', 'sawtooth'];
    return {
        type: [defaultType, ...types.filter(t => t != defaultType)],
    }
}

function getSynthNames() {
    return ['Synth', 'NoiseSynth', 'AMSynth', 'MonoSynth', 'DuoSynth'];
}

function getSynthDefaults(synthName) {
    switch (synthName) {
        default: return null;

        case 'Synth': return {
            oscillator: defaultOscillator('sine'),
            envelope: defaultEnvelope()
        };

        case 'NoiseSynth': return {
            noise: {
                type: ["white", "brown", "pink"]
            },
            envelope: defaultEnvelope({
                sustain: 0,
            }, ['release']),
        };

        case 'AMSynth': return {
            s__harmonicity: [3, 0],
            s__detune: Detune(0),
            oscillator: defaultOscillator('sine'),
            modulation: defaultOscillator('square'),
            envelope: defaultEnvelope({
                attack: 0.01,
                decay: 0.01,
                sustain: 1,
                release: 0.5,
            }),
            modulationEnvelope: defaultEnvelope({
                attack: 0.5,
                decay: 0,
                sustain: 1,
                release: 0.5
            }),
        };

        case 'MonoSynth': return {
            s__volume: Decibel(-25),
            s__detune: Detune(0),
            oscillator: defaultOscillator('square'),
            filter: {
                Q: Positive(6, 3),
                type: [
                    'lowpass', 'highpass', 'bandpass',
                    'lowshelf', 'highshelf', 'notch',
                    'allpass', 'peaking'
                ],
                rolloff: [
                    '-12', '-24', '-48', '-96'
                ]
            },
            envelope: defaultEnvelope({
                attack: 0.005,
                decay: 0.1,
                sustain: 0.9,
                release: 1,
            }),
            filterEnvelope: filterEnvelope({
                attack: 0.06,
                decay: 0.2,
                sustain: 0.5,
                release: 2,
                baseFrequency: 200,
                octaves: 7,
                exponent: 2
            })
        };

        case 'DuoSynth': return {
            s__vibratoAmount: [0.5, 0],
            s__vibratoRate: Positive(5, 1),
            s__harmonicity: [1.5, 0],
            voice0: {
                s__frequency: Frequency(261),
                ...getSynthDefaults('MonoSynth'),
            },
            voice1: {
                s__frequency: Frequency(261),
                ...getSynthDefaults('MonoSynth'),
            },
        };
    }
}

const translations = {
    ru: {
        Synth: 'Волна',
        NoiseSynth: 'Шум',
        AMSynth: 'Двойная волна',
        MonoSynth: 'Волна с фильтром',
        DuoSynth: 'Двойная волна с фильтром',

        value: 'Величина',
        s__volume: 'Громкость',
        s__frequency: 'Частота',
        filter: 'Фильтр',
        baseFrequency: 'Базовая частота',
        octaves: 'Октавы',
        exponent: 'Экспонента',
        rolloff: 'Спад частоты',

        s__vibratoAmount: 'Колчисетво вибрато',
        s__vibratoRate: 'Скорость вибрато',

        oscillator: 'Генератор волны',
        type: 'Тип',
        sine: 'Синусоид',
        square: 'Квадратная',
        triangle: 'Треугольная',
        sawtooth: 'Пила',

        envelope: 'Кривая громкости',
        filterEnvelope: 'Кривая фильтра',
        attack: 'Атака',
        decay: 'Спад',
        sustain: 'Поддерживание',
        release: 'Отпускание',

        noise: 'Шум',
        white: 'Белый',
        brown: 'Коричневый',
        pink: 'Розовый',

        s__harmonicity: 'Гармоничность',
        s__detune: 'Расстроенность',
        modulation: 'Модуляция',
        modulationEnvelope: 'Кривая модуляции',

        voice0: 'Первая волна с фильтром',
        voice1: 'Вторая волна с фильтром',

        Q: 'Качество',
    }
}

function translate(value, lang = 'ru') {
    return (translations[lang] || {})[value] || value;
}
