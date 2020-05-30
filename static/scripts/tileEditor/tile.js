class Tile {
    /** @type {Tile[]} */
    static tiles = [];

    /**
     * @param {number} x
     * @param {number} y
     * @param {number} length
     */
    constructor(x, y, length) {
        this.x = x;
        this.y = y;
        this.length = length;
    }

    place() {
        Tile.tiles.push(this);
    }

    remove() {
        const index = Tile.tiles.findIndex(n => n == this);
        Tile.tiles.splice(index, 1);
    }

    /**
     * @returns {boolean}
     */
    checkCollision() {
        const related_tiles = Tile.tiles.filter(tile => this.y == tile.y && this.x < tile.x);
        return related_tiles.some(tile => this.x + this.length > tile.x);
    }
}
