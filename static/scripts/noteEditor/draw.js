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

var notesPlaceLayer = new paper.Layer({
    name: 'notesPlace',
    children: [
        new paper.Path.Rectangle({
            size: project.view.size,
            fillColor: 'black',
            opacity: 0,
        })
    ]
});

var notesLayer = new paper.Layer({
    name: 'notes'
});

/** @type {paper.Point} */
var mouseCellPoint;

var noteBlueprint = new paper.Path.Rectangle({
    size: cellSize,
    strokeWidth: 2,
    strokeScaling: false,
    opacity: 0,
});

notesPlaceLayer.addChild(noteBlueprint);

onInstrumentSelected = function () {
    noteBlueprint.fillColor = new paper.Color(currentInstrument.notesColor);
    noteBlueprint.strokeColor = noteBlueprint.fillColor.clone();
    noteBlueprint.strokeColor.brightness -= 0.4;
}

var placing = false;
var deleting = false;

/** @param {paper.MouseEvent} mouseEvent */
function calcMouseCellPoint(mouseEvent) {
    return (mouseEvent.point / cellSizePoint).floor();
}

function resetBlueprint() {
    noteBlueprint.bounds.width = cellSize.width;
    noteBlueprint.position = (mouseCellPoint + 0.5) * cellSizePoint;
}

notesPlaceLayer.onMouseDown = function (event) {
    placing = event.event.button == 0;
    deleting = event.event.button == 2;
    if (placing) {
        noteBlueprint.note = MusicNote.makeNoteFromPath(noteBlueprint, cellSize);
    }
}

function placeNote(note) {
    var clone = noteBlueprint.clone();
    clone.opacity = 1;
    notesLayer.addChild(clone);

    if (!note) {
        note = MusicNote.place(noteBlueprint.note);
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
        var length = mouseCellPoint.x - noteBlueprint.note.time + 1;
        if (length >= 1 && mouseCellPoint.x < gridSize.width) {
            noteBlueprint.note.length = length;
            if (!noteBlueprint.note.checkIntersections()) {
                noteBlueprint.bounds.width = length * cellSize.width;
                document.body.style.cursor = 'e-resize';
            }
        }
    }
    else {
        if (deleting) {
            var hit = notesLayer.hitTest(event.point);
            if (hit) {
                hit.item.onClick({ event: { button: 2 } });
            }
        }
        resetBlueprint();
    }
}

project.view.onMouseUp = function (event) {
    if (placing && event.event.button == 0) {
        placing = false;
        document.body.style.cursor = null;
        placeNote();
        stop();
        noteBlueprint.note.playPreview();
        resetBlueprint();
    }
    else if (event.event.button == 1) {
        play(calcMouseCellPoint(event).x);
    }
    deleting = false;
}

notesPlaceLayer.onMouseEnter = function () {
    noteBlueprint.opacity = 0.5;
}

notesPlaceLayer.onMouseLeave = function () {
    if (!placing) {
        noteBlueprint.opacity = 0;
    }
}

//#endregion

//#region load notes

var initialNotesGrouped = groupBy(musicNotes, 'instrumentName');
Object.keys(instruments).forEach(function (instrName) {
    if (!initialNotesGrouped[instrName]) return;
    currentInstrument = instruments[instrName];
    onInstrumentSelected();
    initialNotesGrouped[instrName].forEach(function (note) {
        noteBlueprint.position = (new paper.Point(
            note.time, (octaves + octavesFrom - note.octave - 1) * noteNotations.length + noteNotations.length - note.notation
        ) + onePoint / 2) * cellSizePoint;
        noteBlueprint.bounds.width = note.length * cellSize.width;
        noteBlueprint.note = MusicNote.makeNoteFromPath(noteBlueprint, cellSize);
        placeNote(noteBlueprint.note);
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

notesPlaceLayer.addChild(playhead);

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
