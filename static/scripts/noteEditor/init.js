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

window.addEventListener('tileEditorInit', event => {
    let firstInstr = instruments.firstInstrument;
    if (firstInstr === undefined) {
        firstInstr = { name: allInstrumentNames[0] };
    }
    instrSelect.value = firstInstr.name;
    instrSelect.onchange();

    onInstrumentSelected = () => {
        const tileHint = event.detail.hint;
        tileHint.fillColor = new paper.Color(currentInstrument.notesColor);
        tileHint.strokeColor = tileHint.fillColor.clone();
        tileHint.strokeColor.brightness -= 0.4;
    };
});

const instrSelect = document.querySelector('#instrumentSelect');
instrSelect.onchange = function () {
    instruments.loadInstrument(this.value).then(instr => {
        currentInstrument = instr;
        onInstrumentSelected.call(window);
    });
};

window.addEventListener('tilePlaced', ({ detail: { tile, path, hint } }) => {
    hint.bounds.width = cellSize.width;
})
