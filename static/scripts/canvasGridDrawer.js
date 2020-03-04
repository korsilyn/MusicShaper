class CanvasGridDrawer {
    /**
     * @param {CanvasGrid} canvasGrid
     */
    constructor(canvasGrid) {
        this.canvasGrid = canvasGrid;

        this.cellValueToDraw = false;

        this.onstartdraw = null;
        this.onenddraw = null;

        this.canvasGrid.canvas.onmousedown = (event) => {
            if (event.which != 1) return;
            let { x, y } = this.getMouseGridPosition(event);
            this.cellValueToDraw = !this.canvasGrid.getCell(x, y);
            if (this.onstartdraw) {
                this.onstartdraw(x, y, this.cellValueToDraw);
            }
            
            this.drawCell(x, y);

            this.canvasGrid.canvas.onmousemove = onmousemove;
            window.addEventListener('mouseup', onmouseup);
        }
        
        const onmouseup = (event) => {
            if (event.which == 1) {
                this.canvasGrid.canvas.onmousemove = null;
                if (this.onenddraw) {
                    this.onenddraw();
                }
                window.removeEventListener('mouseup', onmouseup);
            }
        }

        const onmousemove = (event) => {
            if (event.which == 1) {
                let { x, y } = this.getMouseGridPosition(event);
                this.drawCell(x, y);
            }
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
        if (this.canvasGrid.setCell(x, y, this.cellValueToDraw) && this.canvasGrid.cellsToRender.length > 0) {
            this.canvasGrid.render();
        }
    }
}