/// <reference path="../../libs/@types/paper.d.ts" />

const container = document.getElementById('_mainContainer');
container.classList.remove('container');

/** @type {HTMLCanvasElement} */
const canvas = document.querySelector(`canvas#mainCanvas`);

const docStyle = getComputedStyle(document.body);

function getPxVar(name) {
    return Number(docStyle.getPropertyValue(name).replace('px', ''));
}

var cellSize = new paper.Size({
    width: getPxVar('--cell-width'),
    height: getPxVar('--cell-height'),
});

window.onresize = function () {
    const sidebar = document.querySelector('side-bar');

    container.style = `
        width: ${document.body.clientWidth - sidebar.clientWidth}px;
        height: inherit;
    `;
}

window.addEventListener('beforeInstrumentLoad', function () {
    canvas.style.visibility = 'hidden';
    document.body.style.cursor = 'wait';
});

window.addEventListener('instrumentLoad', function () {
    canvas.style.visibility = 'visible';
    document.body.style.cursor = null;
});
