/// <reference path="../../libs/@types/Tone.d.ts" />

document.querySelector('#projBpm').onchange = function () {
    if (this.value < 32) this.value = 32;
    if (this.value > 999) this.value = 999;
    Tone.Transport.bpm.value = this.value;
};

/** @type {string[]} */
var allInstrumentNames = JSON.parse(document.getElementById('allInstrumentNames').innerText);

var instruments = new InstrumentStorage(
    JSON.parse(document.getElementById('usedInstruments').innerText)
);

var currentInstrument = {};

var onInstrumentSelected = () => {};

function loadFirstInstrument() {
    let firstInstr = instruments.firstInstrument;
    if (firstInstr === undefined) {
        firstInstr = { name: allInstrumentNames[0] };
    }
    instrSelect.value = firstInstr.name;
    instrSelect.onchange();
}

const instrSelect = document.querySelector('#instrumentSelect');
instrSelect.onchange = function () {
    instruments.loadInstrument(this.value).then(instr => {
        currentInstrument = instr;
        onInstrumentSelected.call(window);
    });
};
