class Grid {
    /**
     * @param {number} width 
     * @param {number} height 
     */
    constructor(width, height) {
        if (width <= 0)  throw new Error("Grid.width <= 0");
        if (height <= 0) throw new Error("Grid.height <= 0");

        this.width = width;
        this.height = height;
        
        /** @type {boolean[][]} */
        this.cells = new Array(width);
        for (let x = 0; x < width; x++) {
            this.cells[x] = this.makeColumn(false);
        }
    }

    /**
     * @param {number} x 
     * @param {number} y 
     * @returns {boolean}
     */
    checkBounds(x, y) {
        return x >= 0 && y >= 0 && x < this.width && y < this.height;
    }

    /**
     * @param {boolean} value
     * @returns {boolen[]}
     */
    makeColumn(value) {
        return new Array(this.height).fill(value);
    }

    /**
     * @param {number} x 
     * @param {boolean} [value]
     * @returns {void}
     */
    makeColumnSafe(x, value) {
        if (this.checkBounds(x, 0) && this.cells[x] === undefined) {
            this.cells[x] = this.makeColumn(Boolean(value));
        }
    }

    /**
     * @param {boolean} [value]
     * @returns {void}
     */
    addColumn(value) {
        this.width += 1;
        this.makeColumnSafe(this.width-1, value);
    }

    /**
     * @param {boolean} [value]
     * @returns {void}
     */
    addRow(value) {
        this.height += 1;
        this.cells.forEach(column => {
            column.push(Boolean(value))
        });
    }

    /**
     * @param {number} x 
     * @param {number} y 
     * @returns {boolean}
     */
    getCell(x, y) {
        if (this.checkBounds(x, y)) {
            this.makeColumnSafe(x);
            return this.cells[x][y];
        }
        return false;
    }

    /**
     * @param {number} x 
     * @param {number} y
     * @param {boolean} value
     * @returns {boolen} true if changed
     */
    setCell(x, y, value) {
        if (this.checkBounds(x, y)) {
            this.makeColumnSafe(x);
            let old = this.cells[x][y];
            this.cells[x][y] = value;
            return old !== value;
        }
        return false;
    }
}