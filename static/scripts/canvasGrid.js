class CanvasGrid extends Grid {
    /**
     * @param {number} width 
     * @param {number} height 
     * @param {HTMLCanvasElement} canvas 
     */
    constructor(width, height, canvas) {
        super(width, height);
        this.canvas = canvas;
        this.canvas.onresize = this.onresize;
        this.ctx = this.canvas.getContext('2d');
        this.cellsToRender = 'all';

        this.onresize();

        this.canvas.onmousedown = (event) => {
            this.onmousedown(event);
        }

        this.canvas.onmousemove = (event) => {
            this.onmousemove(event);
        }
    }

    onresize() {
        this.canvas.width = this.canvas.clientWidth;
        this.canvas.height = this.canvas.clientHeight;

        this.cellWidth = Math.floor(canvas.width / this.width);
        this.cellHeight = Math.floor(canvas.height / this.height);

        this.cellsToRender = 'all';
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
        if (super.setCell(x, y, value)) {
            this.cellsToRender.push({ x, y });
        }
    }

    /**
     * @param {MouseEvent} event
     * @returns {void} 
     */
    onmousedown(event) {
        const rect = this.canvas.getBoundingClientRect();
        const gx = Math.trunc((event.clientX - rect.left) / this.cellWidth);
        const gy = Math.trunc((event.clientY - rect.top) / this.cellHeight);
        this.setCell(gx, gy, true);
    }

    /**
     * @param {MouseEvent} event
     * @returns {void} 
     */
    onmousemove(event) {
        if (event.which == 1) {
            this.canvas.onmousedown(event);
        }
    }

    /**
     * @returns {void}
     */
    render() {
        if (this.cellsToRender.length == 0) {
            return;
        }

        this.ctx.fillStyle = 'black';
        this.ctx.lineWidth = 0.32;

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