/// <reference path="../tileEditor/tile.js" />
/// <reference path="../instruments.js" />

class MusicNote {
    /**
     * @param {Instrument} instrument
     * @param {number} time
     * @param {number} y
     * @param {number} length
     */
    constructor(instrument, time, y, length) {
        this.time = time;
        this.length = length;
        this.instrument = instrument;
        this.notation = noteNotations.length - y % noteNotations.length;
        this.octave = octavesFrom + octaves - Math.floor(y / noteNotations.length) - 1;
    }

    get instrumentName() {
        return this.instrument.name;
    }

    get duration() {
        return new Tone.Time('16n').toSeconds() * this.length;
    }

    get letterNotation() {
        return noteNotations[this.notation - 1] + this.octave;
    }

    playPreview(time = undefined) {
        let args;
        if (this.instrument instanceof Tone.PolySynth) {
            args = [[this.letterNotation], this.duration, time];
        }
        if (this.instrument instanceof Tone.NoiseSynth) {
            args = [this.duration, time];
        }
        else {
            args = [this.letterNotation, this.duration, time];
        }
        this.instrument.triggerAttackRelease.apply(this.instrument, args);
    }

    get json() {
        return JSON.stringify({
            time: this.time,
            length: this.length,
            octave: this.octave,
            notation: this.notation,
            instrument: this.instrument.id,
        });
    }

    /**
     * @param {Tile} tile
     * @param {Instrument} instrument
     * @returns {MusicNote}
     */
    static fromTile(tile, instrument) {
        return new MusicNote(instrument, tile.x, tile.y, tile.length);
    }
}
