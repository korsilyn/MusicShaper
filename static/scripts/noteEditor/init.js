/// <reference path="../../libs/@types/Tone.d.ts" />

document.querySelector('#projBpm').onchange = function () {
    if (this.value < 32) this.value = 32;
    if (this.value > 999) this.value = 999;
    Tone.Transport.bpm.value = Number(this.value);
};

var octaves = 6;
var octavesFrom = 2;

var noteNotations = [
    'C', 'C#',
    'D', 'D#',
    'E',
    'F', 'F#',
    'G', 'G#',
    'A', 'A#',
    'B',
];

var noteNotationsTotalLenght = noteNotations.length * octaves;

var allInstrumentNames = JSON.parse(document.getElementById('allInstrumentNames').innerText);

var instruments = JSON.parse(document.getElementById('usedInstruments').innerText);
for (const name in instruments) {
    instruments[name] = makeSynth(instruments[name]);
}

var currentInstrument = {};

var onInstrumentSelected = () => {};

function loadFirstInstrument() {
    loadInstrument(allInstrumentNames[0]).then(instr => {
        currentInstrument = instr;
        onInstrumentSelected.call(window);
    });
}

const instrSelect = document.querySelector('#instrumentSelect');
instrSelect.onchange = function () {
    loadInstrument(this.value).then(instr => {
        currentInstrument = instr;
        onInstrumentSelected.call(window);
    });
};
instrSelect.onchange();
