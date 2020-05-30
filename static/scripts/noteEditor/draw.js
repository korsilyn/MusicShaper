/// <reference path="../../libs/@types/paper.d.ts" />
/// <reference path="../../libs/@types/Tone.d.ts" />

/** @type {paper.Project} */
var project;

var onePoint = new paper.Point(1, 1);

//#region grid

var gridLayer = project.activeLayer;
gridLayer.name = 'grid';

var gridSize = new paper.Size(window.patternDuration, noteNotationsTotalLenght);

var cellSizePoint = new paper.Point(cellSize.width, cellSize.height);

var gridRealSize = gridSize * cellSize;
project.view.viewSize.set({
    width: gridRealSize.width,
    height: gridRealSize.height,
});

window.onresize();

//#endregion

//#region notes

var tilePlaceLayer = new paper.Layer({
    name: 'notesPlace',
    children: [
        new paper.Path.Rectangle({
            size: project.view.size,
            fillColor: 'black',
            opacity: 0,
        })
    ]
});

var tilesLayer = new paper.Layer({
    name: 'notes'
});

/** @type {paper.Point} */
var mouseCellPoint;

var tileHint = new paper.Path.Rectangle({
    size: cellSize,
    strokeWidth: 2,
    strokeScaling: false,
    opacity: 0,
});

tileHint.pivot = tileHint.bounds.topLeft;

tilePlaceLayer.addChild(tileHint);

onInstrumentSelected = function () {
    tileHint.fillColor = new paper.Color(currentInstrument.notesColor);
    tileHint.strokeColor = tileHint.fillColor.clone();
    tileHint.strokeColor.brightness -= 0.4;
}

var placing = false;
var deleting = false;

/** @param {paper.MouseEvent} mouseEvent */
function calcMouseCellPoint(mouseEvent) {
    return (mouseEvent.point / cellSizePoint).floor();
}

function resetHint() {
    tileHint.bounds.width = cellSize.width;
    tileHint.position = mouseCellPoint * cellSizePoint;
}

tilePlaceLayer.onMouseDown = function (event) {
    placing = event.event.button == 0;
    deleting = event.event.button == 2;
    if (placing) {
        tileHint.note = MusicNote.makeNoteFromPath(tileHint, cellSize);
    }
}

function placeTile(note) {
    var clone = tileHint.clone();
    clone.opacity = 1;
    tilesLayer.addChild(clone);

    if (!note) {
        note = MusicNote.place(tileHint.note);
    }

    clone.onClick = function (event) {
        if (event.event.button == 2) {
            note.remove();
            clone.remove();
        }
    }
}

/** @param {paper.MouseEvent} event */
project.view.onMouseMove = function (event) {
    mouseCellPoint = calcMouseCellPoint(event);
    if (placing) {
        var length = mouseCellPoint.x - tileHint.note.time + 1;
        if (length >= 1 && mouseCellPoint.x < gridSize.width) {
            tileHint.note.length = length;
            if (!tileHint.note.checkIntersections()) {
                tileHint.bounds.width = length * cellSize.width;
                document.body.style.cursor = 'e-resize';
            }
        }
    }
    else {
        if (deleting) {
            var hit = tilesLayer.hitTest(event.point);
            if (hit) {
                hit.item.onClick({ event: { button: 2 } });
            }
        }
        resetHint();
    }
}

project.view.onMouseUp = function (event) {
    if (placing && event.event.button == 0) {
        placing = false;
        document.body.style.cursor = null;
        placeTile();
        stop();
        tileHint.note.playPreview();
        resetHint();
    }
    else if (event.event.button == 1) {
        play(calcMouseCellPoint(event).x);
    }
    deleting = false;
}

tilePlaceLayer.onMouseEnter = function () {
    tileHint.opacity = 0.5;
}

tilePlaceLayer.onMouseLeave = function () {
    if (!placing) {
        tileHint.opacity = 0;
    }
}

//#endregion

//#region load notes

var initialNotesGrouped = groupBy(Tile.tiles, 'instrumentName');
instruments.instrumentNames.forEach(function (instrName) {
    if (!initialNotesGrouped[instrName]) return;
    currentInstrument = instruments.getByName(instrName);
    onInstrumentSelected();
    initialNotesGrouped[instrName].forEach(function (note) {
        tileHint.bounds.width = note.length * cellSize.width;
        tileHint.position = new paper.Point(
            note.time,
            (octaves + octavesFrom - note.octave - 1) * noteNotations.length + noteNotations.length - note.notation
        ) * cellSizePoint;
        tileHint.note = note;
        placeTile(tileHint.note);
    });
});

loadFirstInstrument();

//#endregion

//#region playhead

var playhead = new paper.Path.Rectangle({
    fillColor: 'rgba(54, 255, 47, 0.4)',
    width: cellSize.width,
    height: gridRealSize.height,
    visible: false,
});

playhead.pivot = playhead.bounds.topLeft;

tilePlaceLayer.addChild(playhead);

window.showPlayhead = function () {
    playhead.visible = true;
}

window.hidePlayhead = function () {
    playhead.visible = false;
}

window.movePlayheadTo = function (xCell) {
    playhead.position.x = xCell * cellSize.width;
}

//#endregion
