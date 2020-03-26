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

        this.oncellupdate = null;
        this.onclear = null;
        
        /** @type {boolean[][]} */
        this.rows = [];
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
        this.rows.forEach(column => column.length = this.width);
    }

    /**
     * @param {number} x 
     * @param {number} y 
     * @returns {boolean}
     */
    getCell(x, y) {
        if (this.checkBounds(x, y)) {
            if (this.rows[y]) {
                return Boolean(this.rows[y][x]);
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
            if (!this.rows[y]) this.rows[y] = [];
            if (Boolean(this.rows[y][x]) != value) {
                if (value) {
                    this.rows[y][x] = value;
                }
                else {
                    delete this.rows[y][x];
                }
                if (this.oncellupdate) {
                    this.oncellupdate(x, y, Boolean(value));
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
        const oldLength = this.rows.length;
        this.rows = [];
        if (this.onclear) {
            this.onclear();
        }
        return oldLength != 0;
    }
}