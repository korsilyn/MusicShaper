class CanvasGrid extends Grid {
    /**
     * @param {HTMLCanvasElement} canvas 
     * @param {number} width 
     * @param {number} height 
     * @param {number} cellWidth 
     * @param {number} cellHeight 
     */
    constructor(canvas, width, height, cellWidth, cellHeight, options={}) {
        super(width, height);
        this.canvas = canvas;
        this.cellWidth = cellWidth;
        this.cellHeight = cellHeight;
        this.options = {
            emptyColor: options.emptyColor || 'white',
            gridColor: options.gridColor || 'black',
            toggledColor: options.toggledColor || 'black',
        }

        if (!options.readonly) {
            this.painter = new CanvasGridPainter(this);
        }

        this.ctx = this.canvas.getContext('2d');

        this.canvas.ondragstart = () => false;

        this.canvas.onresize = () => {
            this.canvas.width = this.cellWidth * this.width;
            this.canvas.height = this.cellHeight * this.height;
            this.cellsToRender = 'all';
            this.render();
        }

        this.canvas.onresize();

        this.oncellupdate = null;

    }

    /**
     * @returns {void}
     */
    addColumn() {
        super.addColumn();
        this.onresize();
    }

    /**
     * @returns {void}
     */
    addRow() {
        super.addRow(false);
        this.onresize();
    }

    /**
     * @param {number} x 
     * @param {number} y
     * @param {boolean} value
     * @returns {void}
     */
    setCell(x, y, value) {
        let r;
        if (r = super.setCell(x, y, value)) {
            this.cellsToRender.push({ x, y });
            if (this.oncellupdate) {
                this.oncellupdate(x, y, value);
            }
        }
        return r;
    }

    /**
     * @returns {void}
     */
    clear() {
        let r = super.clear();
        if (r) {
            this.cellsToRender = 'all';
            this.render();
        }
        return r;
    }

    /**
     * @returns {void}
     */
    render() {
        if (this.cellsToRender.length == 0) {
            return;
        }

        this.ctx.lineCap = 'square';
        this.ctx.lineWidth = 0.5;
        this.ctx.strokeStyle = this.options.gridColor;

        if (this.cellsToRender == 'all') {
            this.renderAll();
            this.cellsToRender = [];
            return;
        }

        while (this.cellsToRender.length > 0) {
            const cell = this.cellsToRender.shift();
            this.renderCell(cell.x, cell.y);
        }
    }

    /**
     * @param {number} x 
     * @param {number} y 
     */
    renderEmptyCell(x, y) {
        let rx = x * this.cellWidth;
        let ry = y * this.cellHeight;
        this.ctx.fillStyle = this.options.emptyColor;
        this.ctx.fillRect(rx, ry, this.cellWidth, this.cellHeight);
        this.ctx.strokeRect(rx, ry, this.cellWidth, this.cellHeight);
    }

    /**
     * @param {number} x 
     * @param {number} y 
     */
    renderToggledCell(x, y) {
        let rx = x * this.cellWidth;
        let ry = y * this.cellHeight;
        this.ctx.fillStyle = this.options.toggledColor;
        this.ctx.fillRect(rx+0.5, ry+0.5, this.cellWidth-1, this.cellHeight-1);
    }

    /**
     * @param {number} x 
     * @param {number} y 
     */
    renderCell(x, y) {
        if (this.getCell(x, y)) {
            this.renderToggledCell(x, y);
        }
        else {
            this.renderEmptyCell(x, y);
        }
    }

    renderAll() {
        for (let x = 0; x < this.width; x++) {
            for (let y = 0; y < this.height; y++) {
                this.renderCell(x, y);
            }
        }
    }
}