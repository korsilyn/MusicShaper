class MusicPatternGrid {
    /**
     * @param {HTMLCanvasElement} cheatsheetCanvas 
     * @param {HTMLCanvasElement} trackCanvas 
     * @param {{0: string, 1: number}[]} notes 
     * @param {number} length
     * @param {number} cellWidth
     * @param {number} cellHeight
     * @param {any} soundData sound data from Pizzicato.js
     */
    constructor(cheatsheetCanvas, trackCanvas, notes, length, cellWidth, cellHeight, soundData) {
        this.notes = notes;

        this.cheatcheetGrid = new CanvasGrid(cheatsheetCanvas, 1, notes.length, cellWidth, cellHeight, {
            readonly: true,
            emptyColor: 'lightgray'
        });

        this.trackGrid = new CanvasGrid(trackCanvas, length, notes.length, cellWidth, cellHeight, {
            toggledColor: '#ff173e'
        });

        this.sound = new Pizzicato.Sound(soundData);

        if (soundData.options && soundData.options.volume) {
            this.sound.volume = soundData.options.volume;
        }

        this.trackGrid.oncellupdate = (x, y, value) => {
            if (value) {
                if (soundData.source == 'wave') this.sound.frequency = notes[y][1];
                this.sound.play();
            }
        }

        this.trackGrid.painter.onenddraw = () => {
            this.sound.stop();
        }

        this.renderCheatsheet();
    }

    renderCheatsheet(font='25px Consolas', color='black') {
        const notesCtx = this.cheatcheetGrid.canvas.getContext('2d');
        notesCtx.font = font;
        notesCtx.fillStyle = color;
        for (let i = 0; i < notes.length; i++) {
            notesCtx.fillText(notes[i][0], 4, i * this.cheatcheetGrid.cellHeight + 21);
        }
    }

    /**
     * @param {UIEvent} event 
     */
    onresize(event) {
        this.cheatcheetGrid.canvas.onresize(event);
        this.renderCheatsheet();
        this.trackGrid.canvas.onresize(event);
    }
}