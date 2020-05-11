/// <reference path="../libs/@types/paper.d.ts" />
/// <reference path="../libs/@types/Tone.d.ts" />

/** @type {paper.Project} */
var project;

var onePoint = new paper.Point(1, 1);

//#region grid

var gridLayer = project.activeLayer;
gridLayer.name = 'grid';

var gridSize = new paper.Size(100, window.noteNotations.length);
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

/** @type {{ [id: string]: boolean }} */
var occupiedCells = {};

/** @param {paper.Point} point */
function getCellId(point, offsetX, offsetY) {
    offsetX = offsetX || 0;
    offsetY = offsetY || 0;
    return (point.x + offsetX) + ',' + (point.y + offsetY);
}

/** @param {paper.Path.Rectangle} path */
function NoteRect(path) {
    this.coords = (path.bounds.topLeft / cellSizePoint + onePoint).floor();
    this.length = Math.floor(path.bounds.width / cellSize.width);

    this.cellIds = [];
    for (var i = 0; i < this.length; i++) {
        var id = getCellId(this.coords, i);
        if (!!occupiedCells[id]) {
            return null;
        }
        occupiedCells[id] = this;
        this.cellIds.push(id);
    }

    this.path = path.clone();
    this.path.opacity = 1;

    this.remove = function () {
        for (var i = 0; i < this.cellIds.length; i++) {
            delete occupiedCells[this.cellIds[i]];
        }
        this.path.remove();
    }
}

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
var drag = false;
var dragStartX = 0;
var nextNoteRect = noteRectDefinition.place();
nextNoteRect.opacity = 0;

var dw, newWidth;

/** @param {paper.MouseEvent} event */
noteLayer.onMouseMove = function (event) {
    mouseCellPoint = (event.point / cellSizePoint).floor() * cellSizePoint;
    if (drag) {
        dw = mouseCellPoint.x + cellSize.width - nextNoteRect.bounds.right;
        newWidth = nextNoteRect.bounds.width + dw;
        if (newWidth >= cellSize.width) {
            nextNoteRect.bounds.width = newWidth;
            nextNoteRect.bounds.left = dragStartX;
        }
    }
    else {
        nextNoteRect.position = mouseCellPoint + cellSizePoint / 2;
    }
}

noteLayer.onMouseEnter = function () {
    nextNoteRect.opacity = 0.5;
}

noteLayer.onMouseLeave = function () {
    nextNoteRect.opacity = 0;
}

noteLayer.onMouseDown = function (event) {
    if (event.event.button == 0) {
        drag = true;
        dragStartX = nextNoteRect.bounds.left;
    }
}

noteLayer.onMouseUp = function (event) {
    if (drag) {
        drag = false;
        new NoteRect(nextNoteRect);
        nextNoteRect.bounds.width = cellSize.width;
    }
    else if (event.event.button == 2) {
        var noteRect = occupiedCells[getCellId(mouseCellPoint / cellSizePoint)];
        if (noteRect) {
            noteRect.remove();
        }
    }
}

//#endregion
