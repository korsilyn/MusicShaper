/// <reference path="../../libs/@types/paper.d.ts" />
/// <reference path="../../libs/@types/Tone.d.ts" />

/** @type {paper.Project} */
var project;

var onePoint = new paper.Point(1, 1);

//#region grid

var gridLayer = project.activeLayer;
gridLayer.name = 'grid';

var gridSize = new paper.Size(window.patternDuration, window.noteNotations.length);
var cellSize = new paper.Size(40, 25);

var cellSizePoint = new paper.Point(cellSize.width, cellSize.height);

var gridRealSize = new paper.Size(
    gridSize.width * cellSize.width,
    gridSize.height * cellSize.height
);

project.view.viewSize.set({
    width: gridRealSize.width,
    height: gridRealSize.height,
});

window.onresize();

var gridStyle = {
    strokeColor: 'black',
    strokeWidth: 1,
};

var gridVerticalLine = new paper.Path.Line({
    style: gridStyle,
    from: new paper.Point(0, 0),
    to: new paper.Point(0, gridRealSize.height),
    locked: true,
});

var gridHorizontalLine = new paper.Path.Line({
    style: gridStyle,
    from: new paper.Point(0, 0),
    to: new paper.Point(gridRealSize.width, 0),
    locked: true,
});

var gridVLineDefinition = new paper.SymbolDefinition(gridVerticalLine);
var gridHLineDefinition = new paper.SymbolDefinition(gridHorizontalLine);

/** @type {paper.Path} */
var instance;

for (var x = 1; x <= gridSize.width; x++) {
    instance = gridVLineDefinition.place();
    instance.position.x = x * cellSize.width;
    instance.position.y = gridRealSize.height / 2;
}

for (var y = 1; y <= gridSize.height; y++) {
    instance = gridHLineDefinition.place();
    instance.position.y = y * cellSize.height;
    instance.position.x = gridRealSize.width / 2;
}

gridLayer.opacity = 0.5;

var raster = gridLayer.rasterize(undefined);
gridLayer.removeChildren();
gridLayer.addChild(raster);

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
    while (!fillColor || fillColor.brightness < 0.5) {
        var fillColor = paper.Color.random();
    }
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
noteBlueprint.position.x += cellSize.width;

var resizing = false;

/** @param {paper.MouseEvent} mouseEvent */
function calcMouseCellPoint(mouseEvent) {
    return (mouseEvent.point / cellSizePoint).floor();
}

function resetBlueprint(updateWidth) {
    if (updateWidth) {
        noteBlueprint.bounds.width = cellSize.width;
    }
    noteBlueprint.position = (mouseCellPoint + 0.5) * cellSizePoint;
}

notesPlaceLayer.onMouseDown = function (event) {
    resizing = event.event.button == 0;
    if (resizing) {
        noteBlueprint.note = MusicNote.makeNoteFromPath(noteBlueprint, cellSize);
        document.body.style.cursor = 'e-resize';
    }
}

/** @param {paper.MouseEvent} event */
function onMouseMove(event) {
    mouseCellPoint = calcMouseCellPoint(event);
    if (resizing) {
        var length = mouseCellPoint.x - noteBlueprint.note.time + 1;
        if (length >= 1 && mouseCellPoint.x < gridSize.width) {
            noteBlueprint.note.length = length;
            if (!noteBlueprint.note.checkIntersections()) {
                noteBlueprint.bounds.width = length * cellSize.width;
            }
        }
    }
    else {
        resetBlueprint();
    }
}

notesPlaceLayer.onMouseMove = onMouseMove;
notesLayer.onMouseMove = onMouseMove;

project.view.onMouseUp = function (event) {
    if (resizing && event.event.button == 0) {
        resizing = false;

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

        resetBlueprint(true);
    }
}

project.view.onMouseEnter = function () {
    noteBlueprint.opacity = 0.5;
}

project.view.onMouseLeave = function () {
    if (!resizing) {
        noteBlueprint.opacity = 0;
    }
}

document.body.addEventListener('mouseup', function () {
    document.body.style.cursor = '';
});

//#endregion
