class CanvasGrid extends Grid {
    /**
     * @param {number} width 
     * @param {number} height 
     * @param {number} cellWidth 
     * @param {number} cellHeight 
     * @param {HTMLCanvasElement} canvas 
     */
    constructor(width, height, cellWidth, cellHeight, canvas) {
        super(width, height);
        this.cellWidth = cellWidth;
        this.cellHeight = cellHeight;
        this.canvas = canvas;

        this.ctx = this.canvas.getContext('2d');

        this.canvas.onresize = () => {
            this.canvas.width = this.cellWidth * this.width;
            this.canvas.height = this.cellHeight * this.height;
            this.cellsToRender = 'all';
        }

        this.canvas.onresize();

        this.drawer = new CanvasGridDrawer(this);
    }

    /**
     * @returns {void}
     */
    addColumn() {
        super.addColumn(false);
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

        this.ctx.fillStyle = 'black';
        this.ctx.lineWidth = 0.5;

        if (this.cellsToRender == 'all') {
            this.renderAll();
            this.cellsToRender = [];
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
        this.ctx.fillStyle = 'white';
        this.ctx.fillRect(rx, ry, this.cellWidth, this.cellHeight);
        this.ctx.fillStyle = 'black';
        this.ctx.strokeRect(rx, ry, this.cellWidth, this.cellHeight);
    }

    /**
     * @param {number} x 
     * @param {number} y 
     */
    renderToggledCell(x, y) {
        let rx = x * this.cellWidth;
        let ry = y * this.cellHeight;
        this.ctx.fillRect(rx, ry, this.cellWidth, this.cellHeight);
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