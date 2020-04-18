class LayeredCanvas {
    /**
     * @param {string} divId
     * @param {[number, number]} layerSize
     */
    constructor(divId, [layerWidth, layerHeight]) {
        this.div = document.getElementById(divId);

        this.div.style.minWidth = layerWidth + 'px';
        this.div.style.minHeight = layerHeight + 'px';

        this.width = layerWidth;
        this.height = layerHeight;

        /** @type {HTMLCanvasElement[]} */
        this.layers = [].filter.call(this.div.childNodes, (el) => el.tagName == 'CANVAS')

        this.layers.forEach(canvas => {
            canvas.width = layerWidth;
            canvas.height = layerHeight;
        });
    }

    /**
     * @param {number} index
     * @returns {HTMLCanvasElement}
     */
    getLayer(index) {
        return this.layers[index];
    }

    /**
     * @param {number} layerIndex 
     * @returns {CanvasRenderingContext2D}
     */
    getLayerContext(layerIndex) {
        const layer = this.getLayer(layerIndex);
        if (!layer) return null;
        return layer.getContext('2d');
    }
}