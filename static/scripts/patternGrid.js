class PatternGrid extends Grid {
    /**
     * @param {string} divId id of layers div
     * @param {[number, number]} gridSize
     * @param {[number, number]} cellSize
     * @param {Object.<string, string>} colors
     * @param {number} bgLayer
     */
    constructor(divId, [gridWidth, gridHeight], [cellWidth, cellHeight], colors, readonly=false, bgLayer=0) {
        super(gridWidth, gridHeight);

        this.cellWidth = cellWidth;
        this.cellHeight = cellHeight;

        this.canvas = new LayeredCanvas(divId, [ this.width * cellWidth, this.height * cellHeight ]);
        
        this.colors = {
            grid: colors.grid || "lightgray",
            note: colors.note || "black"
        }
        
        this.bgContext = this.canvas.getLayerContext(bgLayer);
        
        this.bgContext.strokeStyle = this.colors.grid;
        this.bgContext.lineWidth = 0.5;
        
        this.notesContext = this.canvas.getLayerContext(bgLayer + 1);
        this.notesContext.fillStyle = this.colors.note;

        if (readonly) return;

        this.oncellupdate = (x, y, value) => {
            const f = value ? this.notesContext.fillRect : this.notesContext.clearRect;
            f.call(this.notesContext, x * this.cellWidth, y * this.cellHeight, this.cellWidth, this.cellHeight);
        };

        this.onclear = () => {
            this.notesContext.clearRect(0, 0, this.canvas.width, this.canvas.height);
        }

        this.mousePainter = new PatternMousePainter(this);
    }

    renderBackground() {
        this.bgContext.beginPath();

        for (let y = 0; y <= this.canvas.height; y += this.cellHeight) {
            this.bgContext.moveTo(0, y);
            this.bgContext.lineTo(this.canvas.width, y);
        }

        for (let x = 0; x <= this.canvas.width; x += this.cellWidth) {
            this.bgContext.moveTo(x, 0);
            this.bgContext.lineTo(x, this.canvas.height);
        }

        this.bgContext.stroke();
    }
}