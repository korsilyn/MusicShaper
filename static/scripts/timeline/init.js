/// <reference path="../../libs/@types/Tone.d.ts" />

document.getElementById('_mainContainer').classList.remove('container');

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
            width: document.querySelector('#mainCanvas').parentElement.clientWidth
        },
    });
});

window.addEventListener('tileEditorInit', () => {
    /** @type {paper.Path.Rectangle} */
    const tileHint = window.getTileHint();
    tileHint.strokeWidth = 0.8;

    patterns.selectPattern(patterns.firstPattern.name);
});

function updateDurationInfo() {
    const durationNotes = calculateDuration();
    document.querySelector('#durationNotes').innerText = durationNotes;
    document.querySelector('#durationSeconds').innerText = ((new Tone.Time('16n').toSeconds()) * durationNotes).toFixed(2);
}

window.addEventListener('tilePlaced', updateDurationInfo);
window.addEventListener('tileRemoved', updateDurationInfo);

/** @type {HTMLCanvasElement} */
const canvas = document.querySelector('#mainCanvas');

window.addEventListener('resize', () => {
    window.setTileEditorSize(canvas.parentElement.clientWidth);
});

/** @type {HTMLLinkElement} */
const backToStartLink = document.querySelector('#backToStartLink');

backToStartLink.onclick = function () {
    window.scrollTimelineToStart();
}

/** @param {'hidden' | 'visible'} visibility */
function setBackToStartLink(visibility) {
    backToStartLink.style.visibility = visibility;
    backToStartLink.previousElementSibling.style.visibility = visibility;
}

window.addEventListener('timelineScrollStart', () => {
    setBackToStartLink('hidden');
});

window.dispatchEvent(new Event('timelineScrollStart'));

window.addEventListener('timelineScrollAway', () => {
    setBackToStartLink('visible');
});

window.calculateDuration = function () {
    if (Tile.tiles.length == 0) return 0;
    return Math.max(...Tile.tiles.map(tile => tile.x + tile.length));
}

var instruments = new InstrumentStorage(
    JSON.parse(document.getElementById('instruments').innerText)
);

var patterns = new PatternStorage(
    JSON.parse(document.getElementById('patternsData').innerText),
    instruments
);
