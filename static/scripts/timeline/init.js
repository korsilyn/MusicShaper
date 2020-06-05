/// <reference path="../../libs/@types/Tone.d.ts" />
/// <reference path="../utils.js" />

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

const sixteenthNote = new Tone.TransportTime('16n');

function updateDurationInfo() {
    const duration = calculateDuration();
    durationNotes.innerText = duration;
    let time = sixteenthNote.toSeconds() * duration;
    durationTime.innerText = String(time).toHHMMSS();
}

window.addEventListener('tilePlaced', updateDurationInfo);
window.addEventListener('tileRemoved', updateDurationInfo);

const noteText = document.querySelector('#noteText');
const timeText = document.querySelector('#timeText');

window.addEventListener('tileHintMoved', ({ detail: { tile } }) => {
    noteText.innerHTML = tile.x + 1;
    timeText.innerHTML = String(sixteenthNote.toSeconds() * (tile.x + 1)).toHHMMSS();
});

window.addEventListener('timelineScrollStart', () => {
    noteText.innerHTML = 0;
    timeText.innerHTML = '00:00:00';
});

//#endregion

//#region save key

window.addEventListener('keydown', (event) => {
    if (event.repeat) return;
    if (event.key == 's' && !event.ctrlKey) {
        document.querySelector('button.saveBtn').click();
    }
});

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

//#region load instances

window.addEventListener('tileEditorInit', () => {
    const instancesData = JSON.parse(document.getElementById('instances').innerText);
    const groupedByPattern = groupBy(instancesData, 'pattern_id');

    const tileHint = window.getTileHint();

    try {
        for (const pattern_id in groupedByPattern) {
            patterns.selectPattern(patterns.getById(pattern_id).name);
            for (const instanceData of groupedByPattern[pattern_id]) {
                tileHint.position.set(
                    instanceData.time * cellSize.width, instanceData.track * cellSize.height,
                );
                tileHint.placeTile();
            }
        }
    }
    catch {
        alert('Произошла ошибка при загрузке таймлайна. Повторите попытку позже');
    }
});

//#endregion

//#region recorder

var recorder = new Recorder('button#recordBtn');

const exportModal = document.querySelector('#audioExportModal');

window.addEventListener('recorded', ({ detail: { blob } }) => {
    document.querySelector('audio').src = URL.createObjectURL(blob);
    $(exportModal).modal();
});

document.querySelector('#publishBtn').addEventListener('click', () => {
    if (!(recorder.recordingBlob instanceof Blob)) return;

    const formData = new FormData();
    formData.append('audio', recorder.recordingBlob);
    formData.append('csrfmiddlewaretoken', window.csrf_token);

    $.ajax({
        method: 'POST',
        url: Urls.reverseUrl('upload_track'),
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        success: data => {
            if (data.success && typeof data.redirectUrl == 'string') {
                window.location.href = data.redirectUrl;
            }
            else {
                alert('Произошла ошибка. Повторите попытку позже');
            }
        },
        error: () => {
            alert('Произошла ошибка. Повторите попытку позже');
        },
    });
});

//#endregion
