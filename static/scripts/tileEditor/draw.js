/// <reference path="../../libs/@types/paper.d.ts" />

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

window.addEventListener('tileEditorInit', function (event) {
    gridSize = new paper.Size(event.detail.grid.width, event.detail.grid.height);
    cellSize = new paper.Size(event.detail.cell.width, event.detail.cell.height);

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

    tileHint.pivot = tileHint.bounds.topLeft;
    tilePlaceLayer.addChild(tileHint);

    allowResize = event.detail.allowResize;
});

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
    var curtain = tilePlaceLayer.children[0];
    curtain.size = project.view.size;
}

var tilesLayer = new paper.Layer({
    name: 'tiles'
});

/** @type {paper.Point} */
var mouseCellPoint;

/** @type {paper.Path.Rectangle} */
var tileHint;

var placing = false;
var deleting = false;

/** @param {paper.MouseEvent} mouseEvent */
function calcMouseCellPoint(mouseEvent) {
    return (mouseEvent.point / cellSizePoint).floor();
}

function resetHint() {
    tileHint.position = mouseCellPoint * cellSizePoint;
}

tilePlaceLayer.onMouseDown = function (event) {
    placing = event.event.button == 0;
    deleting = event.event.button == 2;
    if (placing) {
        window.dispatchEvent(new CustomEvent('tileBeginPlacing', {
            detail: { tileHint }
        }));
    }
}

function placeTile() {
    var clone = tileHint.clone();
    clone.opacity = 1;
    tilesLayer.addChild(clone);

    window.dispatchEvent(new CustomEvent('tilePlaced', {
        detail: { tilePath: clone }
    }));

    clone.onClick = function (event) {
        if (event.event.button == 2) {
            window.dispatchEvent(new CustomEvent('tileRemoved', {
                detail: { tilePath: clone }
            }));
            clone.remove();
        }
    }
}

/** @param {paper.MouseEvent} event */
project.view.onMouseMove = function (event) {
    mouseCellPoint = calcMouseCellPoint(event);
    if (placing && allowResize) {
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
        placeTile();
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
