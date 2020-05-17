/// <reference path="../../libs/@types/Tone.d.ts" />

document.querySelector('#projBpm').onchange = function () {
    if (this.value < 32) this.value = 32;
    if (this.value > 999) this.value = 999;
    Tone.Transport.bpm.value = Number(this.value);
};

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
