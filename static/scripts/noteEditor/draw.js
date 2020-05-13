/// <reference path="../../libs/@types/paper.d.ts" />
/// <reference path="../../libs/@types/Tone.d.ts" />

/** @type {paper.Project} */
var project;

var onePoint = new paper.Point(1, 1);

//#region grid

var gridLayer = project.activeLayer;
gridLayer.name = 'grid';

var gridSize = new paper.Size(window.patternDuration, window.noteNotations.length);

window.cellSize = cellSize;

var cellSizePoint = new paper.Point(cellSize.width, cellSize.height);

/** @type {paper.Size} */
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

function makeNotePath() {
    var fillColor = new paper.Color(currentInstrument._notesColor || 'red');
    var strokeColor = fillColor.clone();
    strokeColor.brightness -= 0.4;
    return new paper.Path.Rectangle({
        size: cellSize,
        fillColor: fillColor,
        strokeColor: strokeColor,
        strokeWidth: 2,
        strokeScaling: false
    });
}

/** @type {paper.Point} */
var mouseCellPoint;

/** @type {paper.Path.Rectangle} */
var noteBlueprint = makeNotePath();
notesPlaceLayer.addChild(noteBlueprint);
noteBlueprint.opacity = 0;

onInstrumentSelected = function () {
    noteBlueprint.fillColor = currentInstrument._notesColor;
}

loadFirstInstrument();

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

        /** @type {paper.Path} */
        var clone = noteBlueprint.clone();
        notesLayer.addChild(clone);
        clone.opacity = 1;

        var note = MusicNote.register(noteBlueprint.note);

        clone.onClick = function (event) {
            if (event.event.button == 2) {
                note.remove();
                clone.remove();
            }
        }

        resetBlueprint();
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
