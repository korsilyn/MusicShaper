class CanvasGridDrawer {
    /**
     * @param {CanvasGrid} canvasGrid
     */
    constructor(canvasGrid) {
        this.canvasGrid = canvasGrid;

        this.isDrawing = false;
        this.cellValueToDraw = false;

        this.canvasGrid.canvas.onmousedown = (event) => {
            if (event.which != 1) return;
            let { x, y } = this.getMouseGridPosition(event);
            this.cellValueToDraw = !this.canvasGrid.getCell(x, y);
            this.isDrawing = true;
            this.drawCell(x, y);
        }

        this.canvasGrid.canvas.onmousemove = (event) => {
            if (this.isDrawing && event.which == 1) {
                let { x, y } = this.getMouseGridPosition(event);
                this.drawCell(x, y);
            }
        }

        this.canvasGrid.canvas.onmouseup = (event) => {
            if (event.which != 1) this.isDrawing = false;
        }
    }

    /**
     * @param {MouseEvent} event 
     */
    getMouseGridPosition(event) {
        const rect = this.canvasGrid.canvas.getBoundingClientRect();
        return {
            x: Math.trunc((event.clientX - rect.left) / this.canvasGrid.cellWidth),
            y: Math.trunc((event.clientY - rect.top) / this.canvasGrid.cellHeight),
        }
    }

    /**
     * @param {number} x 
     * @param {number} y 
     */
    drawCell(x, y) {
        this.canvasGrid.setCell(x, y, this.cellValueToDraw);
    }
}