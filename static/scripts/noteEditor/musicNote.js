/// <reference path="../tileEditor/tile.js" />
/// <reference path="../instruments.js" />

class MusicNote extends Tile {
    /**
     * @param {Instrument} instrument
     * @param {number} x
     * @param {number} y
     * @param {number} length
     */
    constructor(instrument, x, y, length) {
        super(x, y, length);
        this.instrument = instrument;
        this.notationId = noteNotations.length - y % noteNotations.length;
        this.octave = octavesFrom + octaves - Math.floor(coordY / noteNotations.length) - 1;
    }

    get time() {
        return this.x;
    }

    remove() {
        super.remove();
        stop();
    }

    get instrumentName() {
        return this.instrument.name;
    }

    get duration() {
        return new Tone.Time('16n').toSeconds() * this.length;
    }

    get letterNotation() {
        return noteNotations[this.notationId - 1] + this.octave;
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
            notation: this.notationId,
            instrument: this.instrument.id,
        });
    }
}


/** @type {MusicNote[]} */
var musicNotes = JSON.parse(document.getElementById('musicNotes').innerText)
    .map(n => new MusicNote(
        instruments.getById(n.instrument),
        n.time,
        n.length,
        n.notation,
        n.octave,
    ));
