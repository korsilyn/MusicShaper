/// <reference path="../libs/@types/paper.d.ts" />
/// <reference path="../libs/@types/Tone.d.ts" />

/** @type {paper.Project} */
var project;

//#region grid

var gridLayer = project.activeLayer;
gridLayer.name = 'grid';

var gridSize = new paper.Size(100, window.noteNotations.length);
var cellSize = new paper.Size(50, 25);

var cellSizePoint = new paper.Point(cellSize.width, cellSize.height);

var gridRealSize = new paper.Size(
    gridSize.width * cellSize.width,
    gridSize.height * cellSize.height
);

project.view.viewSize.set({
    width: gridRealSize.width,
    height: gridRealSize.height,
});

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

gridLayer.opacity = 0.2;

//#endregion

//#region notes

var noteLayer = new paper.Layer({
    name: 'notes',
    children: [
        new paper.Path.Rectangle({
            size: gridRealSize,
            fillColor: 'black',
            opacity: 0,
        })
    ]
});

var noteRectangle = new paper.Path.Rectangle({
    layer: noteLayer,
    size: cellSize,
    fillColor: 'red',
    strokeWidth: 2,
    strokeColor: 'darkred',
    strokeScaling: false,
});

noteRectangle.pivot = noteRectangle.bounds.topLeft;

var noteRectDefinition = new paper.SymbolDefinition(noteRectangle);

/** @type {paper.Point} */
var mouseCellPoint;
var nextNoteRect = noteRectDefinition.place();
nextNoteRect.opacity = 0;

/** @param {paper.MouseEvent} event */
noteLayer.onMouseMove = function (event) {
    mouseCellPoint = (event.point / cellSizePoint).floor() * cellSizePoint;
    nextNoteRect.position = mouseCellPoint + cellSizePoint / 2;
}

noteLayer.onMouseEnter = function () {
    nextNoteRect.opacity = 0.5;
}

noteLayer.onMouseLeave = function () {
    nextNoteRect.opacity = 0;
}

//#endregion
