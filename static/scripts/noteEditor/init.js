const container = document.getElementById('_mainContainer');
container.classList.remove('container');

window.onresize = function () {
    const drawScript = document.querySelector('script[type="text/paperscript"]');
    const canvasId = drawScript.getAttribute('canvas');

    const canvas = document.querySelector(`canvas#${canvasId}`);
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

async function loadInstrument(name) {
    try {
        const settings = await requestInstrument(name);
        instrumentSettings[name] = settings;
    }
    catch (err) {
        console.error(`failed to request instrument: ${err}`);
    }
}

var currentInstrument = Object.keys(instrumentSettings)[0];

/** @type {Map<string, MusicNote[]>} */
var musicNotes = new Map();

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

        console.log(this.note, this.octave);

        MusicNote.register(this);
    }

    /**
     * @param {MusicNote} note
     */
    static register(note) {
        if (!musicNotes.has(note.instrument)) {
            musicNotes.set(note.instrument, []);
        }
        musicNotes.get(note.instrument).push(note);
    }

    remove() {
        if (!musicNotes.has(this.instrument)) {
            return;
        }
        const arr = musicNotes.get(this.instrument);
        const index = arr.findIndex(n => n == this);
        arr.splice(index);
    }
}
