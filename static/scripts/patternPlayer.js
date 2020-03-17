class PatternPlayer {
    /**
     * @param {PatternGrid} trackGrid
     * @param {any} synth (Tone.PolySynth)  
     * @param {number} notesCount
     * @param {string} playheadColor
     * @param {string} interval loop interval (Tone.Time)
     * @param {string} noteDuration (Tone.Time)
     */
    constructor(trackGrid, synth, { playheadColor='lightgreen', interval='4n', noteDuration='8n' }) {
        this.trackGrid = trackGrid;
        this.synth = synth;

        this.loop = null;
        this.interval = interval;
        this.noteDuration = noteDuration;
        
        this.playheadColumn = -1;
        this.playheadCtx = trackGrid.canvas.getLayerContext(0);

        this.playheadCtx.fillStyle = playheadColor;
    }

    stop() {
        Tone.Transport.stop(0);
        setTimeout(() => this.hidePlayhead(), 100);
    }

    /**
     * @returns {Object.<string, boolean[]>}
     */
    getUsedRows() {
        return this.trackGrid.rows.reduce((obj, row, y) => {
            if (row.find(cell => Boolean(cell))) obj[notes[y]] = row;
            return obj;
        }, {});
    }

    /**
     * @param {Object.<string, boolean[]>} usedRows 
     * @param {number} column
     * @returns {string[]}
     */
    getNotesToPlay(usedRows, column) {
        const notes = [];
        for (const note in usedRows) {
            const row = usedRows[note];
            if (row[column]) {
                notes.push(note);
            }
        }
        return notes;
    }

    play() {
        const usedRows = this.getUsedRows();

        const rowsCount = Object.keys(usedRows).length;
        if (rowsCount == 0) return;

        /** @type {boolean[][]} */
        const usedRowsNotes = Object.values(usedRows);

        const columnsCount = usedRowsNotes
            .reduce((max, curr) => curr.length > max ? curr.length : max, usedRowsNotes[0].length);

        let column = 0, stopped = false;

        const playColumn = (time) => {
            if (stopped) return;

            if (!this.synth || column >= columnsCount) {
                this.loop.stop(time);

                stopped = true;
                setTimeout(() => {
                    this.loop = null;
                    this.hidePlayhead();
                }, time + 1);

                return;
            }

            const notesToPlay = this.getNotesToPlay(usedRows, column);
            this.synth.triggerAttackRelease(notesToPlay, this.noteDuration, time);

            const pastColumn = column;
            setTimeout(() => {
                this.renderPlayhead(pastColumn);
            }, time - 1);

            column++;
        }

        if (this.loop) {
            this.loop.stop(0);
        }

        this.loop = new Tone.Loop(playColumn, this.interval);

        this.loop.start(0);
        Tone.Transport.start();
    }

    hidePlayhead() {
        if (this.playheadColumn >= 0) {
            this.playheadCtx.clearRect(
                this.playheadColumn * this.trackGrid.cellWidth, 0,
                this.trackGrid.cellWidth, this.trackGrid.canvas.height
            );
            this.playheadColumn = -1;
        }
    }

    /**
     * @param {number} column 
     */
    renderPlayhead(column) {
        this.hidePlayhead();
        if (column < 0) return;

        this.playheadColumn = column;

        this.playheadCtx.fillRect(
            this.playheadColumn * this.trackGrid.cellWidth, 0,
            this.trackGrid.cellWidth, this.trackGrid.canvas.height
        );
    }
}