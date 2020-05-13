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

async function loadInstrument(name) {
    try {
        const settings = await requestInstrument(name);
        instrumentSettings[name] = settings;
        return { name, ...settings };
    }
    catch (err) {
        console.error(`failed to request instrument: ${err}`);
    }
}

var currentInstrument = instrumentSettings[availableInstrumentNames[0]];

/** @type {(() => void) | null} */
var onInstrumentLoaded = null;

if (!currentInstrument) {
    if (availableInstrumentNames.length == 0) {
        alert('В вашем проекте нет музыкальных иснтрументов');
    }
    else {
        loadInstrument(availableInstrumentNames[0]).then(instr => {
            currentInstrument = instrumentSettings[instr.name];
            if (onInstrumentLoaded) {
                onInstrumentLoaded();
            }
        }).catch(() => {
            alert('Произошла ошибка при загрузке музыкального инструмента');
            alert('Попробуйте зайти на эту страницу позже');
        });
    }
}

document.getElementById('instrumentSelect').onchange = function () {
    currentInstrument = instrumentSettings[this.value];
};

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
    }

    remove() {
        if (!musicNotes.has(this.instrument)) {
            return;
        }
        const arr = musicNotes.get(this.instrument);
        const index = arr.findIndex(n => n == this);
        arr.splice(index);
    }

    /**
     * @returns {boolean}
     */
    checkIntersections() {
        const related_notes = (musicNotes.get(this.instrument) || [])
            .filter(n => this.octave == n.octave && this.note == n.note && this.time < n.time);
        return related_notes.some(n => this.time + this.length > n.time);
    }

    /**
     * @param {MusicNote} note
     */
    static register(note) {
        if (!musicNotes.has(note.instrument)) {
            musicNotes.set(note.instrument, []);
        }
        musicNotes.get(note.instrument).push(note);
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
