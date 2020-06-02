/// <reference path="../../libs/@types/Tone.d.ts" />

document.getElementById('_mainContainer').classList.remove('container');

/** @type {HTMLCanvasElement} */
const canvas = document.querySelector('#mainCanvas');

//#region bpm

/** @type {HTMLInputElement} */
var bpmInput = document.querySelector('#projBpm');

Object.defineProperty(bpmInput, 'safeValue', {
    get: function () {
        if (this.value < 32) this.value = 32;
        if (this.value > 999) this.value = 999;
        return Number(this.value);
    }
});

bpmInput.onchange = function () {
    Tone.Transport.bpm.value = this.safeValue;
};

bpmInput.onchange();

//#endregion

//#region pattern selected

document.querySelectorAll('#patterns a').forEach(a => {
    a.onclick = function () {
        patterns.selectPattern(this.querySelector('.card-title').innerText);
    }
    a.style.borderColor = a.getAttribute('data-pattern-color');
});

window.addEventListener('patternSelected', ({ detail: { oldPattern: old, current } }) => {
    if (old) {
        document.querySelector(`a[data-pattern-name="${old.name}"]`).classList.remove('selected');
    }

    document.querySelector(`a[data-pattern-name="${current.name}"]`).classList.add('selected');

    if (!window.getTileHint) return;

    /** @type {paper.Path.Rectangle} */
    const tileHint = window.getTileHint();
    tileHint.fillColor = new paper.Color(current.color);
    tileHint.strokeColor = tileHint.fillColor.clone();
    tileHint.strokeColor.brightness -= 0.4;
    tileHint.bounds.width = cellSize.width * current.duration;
    tileHint.makeTile();
});

//#endregion

//#region tile editor init

window.addEventListener('tileEditorReady', ({ detail: { init } }) => {
    const docStyle = getComputedStyle(document.body);
    const getPxVar = name => Number(docStyle.getPropertyValue(name).replace('px', ''));
    window.cellSize = {
        width: getPxVar('--cell-width'),
        height: getPxVar('--cell-height'),
    };
    init({
        allowResize: false,
        limitByWidth: false,
        grid: {
            width: 128,
            height: 5
        },
        cell: cellSize,
        realCanvasSize: {
            width: canvas.parentElement.clientWidth
        },
    });
});

window.addEventListener('tileEditorInit', () => {
    /** @type {paper.Path.Rectangle} */
    const tileHint = window.getTileHint();
    tileHint.strokeWidth = 0.8;

    patterns.selectPattern(patterns.firstPattern.name);

    canvas.parentElement.style.height = canvas.clientHeight + 'px';
});

//#endregion

//#region project info

function calculateDuration() {
    if (Tile.tiles.length == 0) return 0;
    return Math.max(...Tile.tiles.map(tile => tile.x + tile.length));
}

const durationTime = document.querySelector('#durationTime');
const durationNotes = document.querySelector('#durationNotes');

function updateDurationInfo() {
    const duration = calculateDuration();
    durationNotes.innerText = duration;
    let time = (player.baseTimeSeconds) * duration;
    durationTime.innerText = String(time).toHHMMSS();
}

window.addEventListener('tilePlaced', updateDurationInfo);
window.addEventListener('tileRemoved', updateDurationInfo);

//#endregion

//#region resize event

window.addEventListener('resize', () => {
    window.setTileEditorSize(canvas.parentElement.clientWidth);
});

//#endregion

//#region back to start btn

/** @type {HTMLLinkElement} */
const backToStartLink = document.querySelector('#backToStartLink');

backToStartLink.onclick = function () {
    window.scrollTimelineToStart();
}

/** @param {'hidden' | 'visible'} visibility */
function setBackToStartLink(visibility) {
    if (visibility == 'hidden') visibility = 'none';
    else visibility = 'block';
    backToStartLink.style.display = visibility;
    backToStartLink.previousElementSibling.style.display = visibility;
}

window.addEventListener('timelineScrollStart', () => {
    setBackToStartLink('hidden');
});

window.dispatchEvent(new Event('timelineScrollStart'));

window.addEventListener('timelineScrollAway', () => {
    setBackToStartLink('visible');
});

//#endregion

//#region tile placed

window.addEventListener('tilePlaced', ({ detail: { tile } }) => {
    if (player.isPlaying) player.stop();
    tile.pattern = patterns.current;
});

window.addEventListener('tileRemoved', () => {
    if (player.isPlaying) player.stop();
});

//#endregion

//#region storages

var instruments = new InstrumentStorage(
    JSON.parse(document.getElementById('instruments').innerText)
);

var patterns = new PatternStorage(
    JSON.parse(document.getElementById('patternsData').innerText),
    instruments
);

//#endregion

//#region player

var player = new TimelinePlayer(patterns, 'button.playBtn', 'button.stopBtn', 'button.loopBtn');

window.addEventListener('stop', ({ detail: { reason } }) => {
    if (reason == 'user' || reason == 'end') {
        const time = reason == 'end' ? '+0.3' : undefined;
        for (const i of instruments.instruments.values()) {
            if (i instanceof Tone.PolySynth) i.releaseAll(time);
            else i.triggerRelease(time);
        }
    }
});

//#endregion
