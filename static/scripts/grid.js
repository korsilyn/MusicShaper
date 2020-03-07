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
        this.cells = [];
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
        if (value) {
            return new Array(this.height).fill(value);
        }
        else {
            return [];
        }
    }

    /**
     * @returns {void}
     */
    addColumn() {
        this.width += 1;
        this.cells.forEach(column => column.length = this.width);
    }

    /**
     * @param {number} x 
     * @param {number} y 
     * @returns {boolean}
     */
    getCell(x, y) {
        if (this.checkBounds(x, y)) {
            if (this.cells[y]) {
                return Boolean(this.cells[y][x]);
            }
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
            if (!this.cells[y]) this.cells[y] = [];
            if (Boolean(this.cells[y][x]) != value) {
                if (value) {
                    this.cells[y][x] = value;
                }
                else {
                    delete this.cells[y][x];
                }
                return true;
            }
        }
        return false;
    }

    /**
     * @returns {boolean}
     */
    clear() {
        const oldLength = this.cells.length;
        this.cells = [];
        return oldLength != 0;
    }
}