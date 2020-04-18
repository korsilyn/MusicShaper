class PatternMousePainter {
    /**
     * @param {CanvasPatternGrid} grid
     */
    constructor(grid) {
        this.grid = grid;

        this.cellValueToDraw = false;

        this.onstartdraw = null;
        this.onenddraw = null;

        this.grid.notesContext.canvas.onmousedown = (event) => {
            if (event.which != 1) return;
            let [ x, y ] = this.getMouseGridPosition(event);
            this.cellValueToDraw = !this.grid.getCell(x, y);
            if (this.onstartdraw) {
                this.onstartdraw(x, y, this.cellValueToDraw);
            }
            
            this.drawCell(x, y);

            this.grid.notesContext.canvas.onmousemove = onmousemove;
            window.addEventListener('mouseup', onmouseup);
        }
        
        const onmouseup = (event) => {
            if (event.which == 1) {
                this.grid.notesContext.canvas.onmousemove = undefined;
                if (this.onenddraw) {
                    this.onenddraw();
                }
                window.removeEventListener('mouseup', onmouseup);
            }
        }

        const onmousemove = (event) => {
            if (event.which == 1) {
                let [ x, y ] = this.getMouseGridPosition(event);
                this.drawCell(x, y);
            }
        }
    }

    /**
     * @param {MouseEvent} event 
     */
    getMouseGridPosition(event) {
        const rect = this.grid.notesContext.canvas.getBoundingClientRect();
        return [
            Math.trunc((event.clientX - rect.left) / this.grid.cellWidth),
            Math.trunc((event.clientY - rect.top) / this.grid.cellHeight),
        ]
    }

    /**
     * @param {number} x 
     * @param {number} y 
     */
    drawCell(x, y) {
        this.grid.setCell(x, y, this.cellValueToDraw);
    }
}