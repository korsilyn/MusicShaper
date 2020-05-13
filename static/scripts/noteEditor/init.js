const container = document.getElementById('_mainContainer');
container.classList.remove('container');

/** @type {HTMLCanvasElement} */
const canvas = document.querySelector(`canvas#mainCanvas`);

const docStyle = getComputedStyle(document.body);

function getPxVar(name) {
    return Number(docStyle.getPropertyValue(name).replace('px', ''));
}

var cellSize = new paper.Size({
    width: getPxVar('--cell-width'),
    height: getPxVar('--cell-height'),
});

window.onresize = function () {
    canvas.style.display = 'block';
    canvas.focus();

    const sidebar = document.getElementsByTagName('side-bar').item(0);

    container.style = `
        width: ${document.body.clientWidth - sidebar.clientWidth}px;
        height: inherit;
    `;
}

var octaves = 6;
var octavesFrom = 2;

var baseNoteNotations = [
    'C', 'C#',
    'D', 'D#',
    'E',
    'F', 'F#',
    'G', 'G#',
    'A', 'A#',
    'B',
];

var noteNotations = new Array(octaves).fill(baseNoteNotations)
    .map((arr, i) => arr.map(note => note + (i + octavesFrom))).flat();

var availableInstrumentNames = JSON.parse(
    document.getElementById('allInstrumentNames').innerText
);

var instrumentSettings = JSON.parse(
    document.getElementById('usedInstruments').innerText
);

function requestInstrument(instrumentName) {
    return new Promise((resolve, reject) => {
        $.ajax({
            method: 'GET',
            dataType: 'json',
            url: window.location.href,
            data: {
                csrfmiddlewaretoken: '{{ csrf_token }}',
                operation: 'loadInstrument',
                instrumentName,
            },
            success: (data) => {
                if (data.success && data[instrumentName]) {
                    resolve(data[instrumentName]);
                }
                else {
                    reject('failed');
                }
            },
            error: (e, s, thrownErr) => {
                reject(thrownErr);
            }
        })
    });
}

function delay() {
    return new Promise(resolve => {
        setTimeout(resolve, 2000);
    })
}

/** @param {string} name */
async function loadInstrument(name) {
    try {
        canvas.style.display = 'none';
        document.body.style.cursor = 'wait';
        let settings;
        if (!instrumentSettings[name]) {
            settings = await requestInstrument(name);
            instrumentSettings[name] = settings;
        }
        else {
            settings = instrumentSettings[name];
        }
        canvas.style.display = 'block';
        document.body.style.cursor = null;
        return { name, ...settings };
    }
    catch (err) {
        console.error(`failed to request instrument: ${err}`);
    }
}

/** @type {{}} */
var currentInstrument = {};

/** @type {() => void} */
var onInstrumentSelected = () => {};

function loadFirstInstrument() {
    loadInstrument(availableInstrumentNames[0]).then(instr => {
        currentInstrument = instr;
        onInstrumentSelected.call(window);
    });
}

document.getElementById('instrumentSelect').onchange = function () {
    loadInstrument(this.value).then(instr => {
        currentInstrument = instr;
        onInstrumentSelected.call(window);
    });
};

/** @type {MusicNote[]} */
var musicNotes = [];

class MusicNote {
    /**
     * @param {string} instrument
     * @param {number} pos
     * @param {number} duration
     * @param {number} noteId
     * @param {number} octave
     */
    constructor(instrument, pos, duration, noteId, octave) {
        this.instrument = instrument;
        this.time = pos;
        this.length = duration;
        this.note = noteId;
        this.octave = octave;
    }

    remove() {
        const index = musicNotes.findIndex(n => n == this);
        musicNotes.splice(index);
    }

    /**
     * @returns {boolean}
     */
    checkIntersections() {
        const related_notes = musicNotes.filter(
            n => this.octave == n.octave && this.note == n.note && this.time < n.time
        );
        return related_notes.some(n => this.time + this.length > n.time);
    }

    /**
     * @param {MusicNote} note
     */
    static register(note) {
        musicNotes.push(note);
        return note;
    }

    /**
     * @param {paper.Path.Rectangle} path
     * @param {paper.Size} cellSize
     */
    static makeNoteFromPath(path, cellSize) {
        const coordY = Math.floor(path.bounds.top / cellSize.height);
        return new MusicNote(
            currentInstrument,
            Math.floor(path.bounds.left / cellSize.width),
            Math.floor(path.bounds.width / cellSize.width),
            baseNoteNotations.length - coordY % baseNoteNotations.length,
            octavesFrom + octaves - Math.floor(coordY / baseNoteNotations.length) - 1
        );
    }
}
