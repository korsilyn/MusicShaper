function undefinedOr(v, d) {
    return v === undefined ? d : v;
}

function defaultEnvelope(values={}, remove=[]) {
    let env = {
        attack:  [undefinedOr(values.attack,  0.005),  0],
        decay:   [undefinedOr(values.decay,   0.1),    0],
        sustain: [undefinedOr(values.sustain, 0.3), 0, 1],
        release: [undefinedOr(values.release, 1),      0],
    };
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
    return ['Synth', 'NoiseSynth', 'AMSynth'];
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
            harmonicity: [3, 0],
            detune: [0, 0],
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
    }
}

const translations = {
    ru: {
        Synth: 'Волна',
        NoiseSynth: 'Шум',
        AMSynth: 'Двойная волна',

        oscillator: 'Генератор волны',
        type: 'Тип',
        sine: 'Синусоид',
        square: 'Квадратная',
        triangle: 'Треугольная',
        sawtooth: 'Пила',

        envelope: 'Кривая громкости',
        attack: 'Атака',
        decay: 'Спад',
        sustain: 'Поддерживание',
        release: 'Отпускание',

        noise: 'Шум',
        white: 'Белый',
        brown: 'Коричневый',
        pink: 'Розовый',

        harmonicity: 'Гармоничность',
        detune: 'Расстроенность',
        modulation: 'Модуляция',
        modulationEnvelope: 'Кривая модуляции',
    }
}

function translate(value, lang='ru') {
    return (translations[lang] || {})[value] || value;
}
