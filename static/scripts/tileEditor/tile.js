/// <reference path="../../libs/@types/paper.d.ts" />

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

    /**
     * @param {paper.Path.Rectangle} rect
     * @param {paper.Size} cellSize
     * @returns {Tile}
     */
    static fromPath(rect, cellSize) {
        const pos = rect.bounds.topLeft;
        return new Tile(...[
            pos.x / cellSize.width,
            pos.y / cellSize.height,
            rect.bounds.width / cellSize.width,
        ].map(Math.floor));
    }
}
