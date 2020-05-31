/// <reference path="../../libs/@types/paper.d.ts" />
/// <reference path="tile.js" />

/** @type {paper.Project} */
var project;

var onePoint = new paper.Point(1, 1);

//#region grid

var gridLayer = project.activeLayer;
gridLayer.name = 'grid';

/** @type {paper.Size} */
var gridSize;

/** @type {paper.Size} */
var cellSize;

/** @type {paper.Point} */
var cellSizePoint;

var allowResize = false;

function initTileEditor(options) {
    var grid = options.grid;
    var cell = options.cell;
    var _resize = options.allowResize;

    gridSize = new paper.Size(grid.width, grid.height);
    cellSize = new paper.Size(cell.width, cell.height);

    cellSizePoint = new paper.Point(cellSize.width, cellSize.height);

    var gridRealSize = gridSize * cellSize;
    project.view.viewSize.set({
        width: gridRealSize.width,
        height: gridRealSize.height,
    });

    playhead = new paper.Path.Rectangle({
        fillColor: 'rgba(54, 255, 47, 0.4)',
        width: cellSize.width,
        height: gridRealSize.height,
        visible: false,
    });

    playhead.pivot = playhead.bounds.topLeft;
    tilePlaceLayer.addChild(playhead);

    tileHint = new paper.Path.Rectangle({
        size: cellSize,
        strokeWidth: 2,
        strokeScaling: false,
        opacity: 0,
    });

    tileHint.style.fillColor = 'red';

    tileHint.pivot = tileHint.bounds.topLeft;
    tilePlaceLayer.addChild(tileHint);

    tileHint.placeTile = placeTile;

    allowResize = _resize;

    window.dispatchEvent(new CustomEvent('tileEditorInit', {
        detail: { hint: tileHint }, project: project
    }));
}

//#endregion

//#region notes

var tilePlaceLayer = new paper.Layer({
    name: 'tilePlace',
    children: [
        new paper.Path.Rectangle({
            size: project.view.size,
            fillColor: 'black',
            opacity: 0,
        })
    ]
});

/** @param {paper.Eve} */
project.view.onResize = function (event) {
    tilePlaceLayer.children[0].size = project.view.size;
}

var tilesLayer = new paper.Layer({
    name: 'tiles'
});

/** @type {paper.Point} */
var mouseCellPoint;

/**
 * @typedef {paper.Path.Rectangle & { tile: Tile }} TilePath
 */

/** @type {TilePath} */
var tileHint;

window.getTileHint = function () {
    return tileHint;
}

var placing = false;
var deleting = false;

/** @param {paper.MouseEvent} mouseEvent */
function calcMouseCellPoint(mouseEvent) {
    return (mouseEvent.point / cellSizePoint).floor();
}

function resetHint() {
    tileHint.position = mouseCellPoint * cellSizePoint;
}

paper.Item.prototype.makeTile = function () {
    if (!this.tile || this.id == tileHint.id) {
        this.tile = Tile.fromPath(this, cellSize);
    }
    return this.tile;
}

/** @param {string} type */
paper.Item.prototype.makeEvent = function (type) {
    var tile = this.makeTile();
    return new CustomEvent(type, {
        detail: { tile: tile, path: this, hint: tileHint, project: project }
    });
}

/** @param {string} type */
paper.Item.prototype.dispatchWindowTileEvent = function (type) {
    return window.dispatchEvent(this.makeEvent(type));
}

tilePlaceLayer.onMouseDown = function (event) {
    placing = event.event.button == 0;
    deleting = event.event.button == 2;
    if (placing) {
        tileHint.dispatchWindowTileEvent('tileBeginPlacing');
    }
}

function placeTile() {
    /** @type {TilePath} */
    var clone = tileHint.clone();
    clone.opacity = 1;
    tilesLayer.addChild(clone);

    clone.makeTile();
    clone.tile.place();

    if (allowResize) {
        tileHint.bounds.width = cellSize.width;
    }

    clone.dispatchWindowTileEvent('tilePlaced');

    clone.onClick = function (event) {
        if (event.event.button == 2) {
            clone.dispatchWindowTileEvent('tileRemoved');
            clone.tile.remove();
            clone.remove();
        }
    }
}

/** @param {paper.MouseEvent} event */
project.view.onMouseMove = function (event) {
    mouseCellPoint = calcMouseCellPoint(event);
    if (placing && allowResize) {
        var length = mouseCellPoint.x - tileHint.tile.x + 1;
        if (length >= 1 && mouseCellPoint.x < gridSize.width) {
            tileHint.tile.length = length;
            if (!tileHint.tile.checkCollision()) {
                tileHint.bounds.width = length * cellSize.width;
                tileHint.dispatchWindowTileEvent('tileHintResize');
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
        placeTile();
        resetHint();
    }
    deleting = false;
    window.dispatchEvent(new CustomEvent('tileEditorMouseUp', {
        detail: {
            button: event.event.button,
            cellPoint: mouseCellPoint,
            point: event.point,
            event: event.event,
        }
    }));
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

//#region playhead

/** @type {paper.Path.Rectangle} */
var playhead;

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

window.dispatchEvent(new CustomEvent('tileEditorReady', {
    detail: { init: initTileEditor }
}));
