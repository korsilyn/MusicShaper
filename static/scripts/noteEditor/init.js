/// <reference path="../../libs/@types/Tone.d.ts" />
/// <reference path="../../libs/@types/paper.d.ts" />

//#region container size

const container = document.getElementById('_mainContainer');
container.classList.remove('container');

const sideBar = document.querySelector('side-bar');
window.addEventListener('resize', () => {
    container.style.width = `${document.body.clientWidth - sideBar.clientWidth}px`;
});

window.dispatchEvent(new Event('resize'));

//#endregion

//#region cell size

/** @type {HTMLCanvasElement} */
const canvas = document.querySelector(`canvas#mainCanvas`);

/** @type {paper.Size} */
var cellSize;

(function(){
    const docStyle = getComputedStyle(document.body);
    const getPxVar = name => Number(docStyle.getPropertyValue(name).replace('px', ''));
    cellSize = new paper.Size(
        getPxVar('--cell-width'),
        getPxVar('--cell-height'),
    );
})();

//#endregion

//#region bpm

/** @type {HTMLInputElement} */
var bpmInput = document.querySelector('#projBpm');

Object.defineProperty(bpmInput, 'safeValue', {
    get: function () {
        if (this.value < 32) this.value = 32;
        if (this.value > 999) this.value = 999;
        return this.value;
    }
});

bpmInput.onchange = function () {
    Tone.Transport.bpm.value = this.safeValue;
};

bpmInput.onchange();

//#endregion

//#region events

window.addEventListener('tileEditorReady', event => {
    event.detail.init({
        allowResize: true,
        grid: {
            width: patternDuration,
            height: noteNotationsTotalLenght,
        },
        cell: {
            width: cellSize.width,
            height: cellSize.height,
        },
    });
    window.dispatchEvent(new Event('instrumentSelected'));
});

window.addEventListener('beforeInstrumentLoad', () => {
    canvas.style.visibility = 'hidden';
    document.body.style.cursor = 'wait';
});

window.addEventListener('instrumentLoad', () => {
    canvas.style.visibility = 'visible';
    document.body.style.cursor = null;
});

window.addEventListener('tilePlaced', () => {
    document.body.style.cursor = null;
});

window.addEventListener('tileHintResize', () => {
    document.body.style.cursor = 'e-resize';
});

window.addEventListener('instrumentSelected', () => {
    if (!window.getTileHint) return;
    /** @type {TilePath} */
    const tileHint = window.getTileHint();
    tileHint.style.fillColor = new paper.Color(instruments.current.notesColor);
    tileHint.style.strokeColor = tileHint.style.fillColor.clone();
    tileHint.style.strokeColor.brightness -= 0.4;
});

window.addEventListener('tilePlaced', ({ detail: { tile } }) => {
    tile.note = MusicNote.fromTile(tile, instruments.current);
    if (!window.loadingNotes) {
        if (player.isPlaying) stop();
        tile.note.playPreview();
    }
});

window.addEventListener('tileRemoved', () => {
    if (player.isPlaying) stop();
});

//#endregion

//#region load instruments

var instruments = new InstrumentStorage(
    JSON.parse(document.getElementById('usedInstruments').innerText),
    JSON.parse(document.getElementById('allInstrumentNames').innerText),
);

const instrSelect = document.querySelector('#instrumentSelect');
instrSelect.onchange = function () {
    instruments.loadCurrentInstrument(this.value);
};

//#endregion

//#region player

var player = new NotePlayer(instruments, 'button.playBtn', 'button.stopBtn', 'button.loopBtn');

//#endregion

//#region load notes

window.addEventListener('tileEditorInit', async () => {
    const initialNotes = JSON.parse(document.getElementById('musicNotes').innerText)
        .map(data => new MusicNote(
            instruments.getById(data.instrument),
            data.time,
            (octaves + octavesFrom - data.octave) * noteNotations.length - data.notation,
            data.length,
        ));

    if (initialNotes.length == 0) {
        return;
    }

    window.loadingNotes = true;

    const initialNotesGrouped = groupBy(initialNotes, 'instrumentName');
    const tileHint = window.getTileHint();

    for (const instrName of instruments.instruments.keys()) {
        if (!initialNotesGrouped[instrName]) return;
        await instruments.loadCurrentInstrument(instrName);
        for (const note of initialNotesGrouped[instrName]) {
            tileHint.bounds.width = note.length * cellSize.width;
            tileHint.position.set(
                note.time * cellSize.width,
                ((octaves + octavesFrom - note.octave) * noteNotations.length - note.notation) * cellSize.height,
            );
            tileHint.placeTile();
        }
    }

    window.loadingNotes = false;
    instrSelect.onchange();
});

//#endregion
