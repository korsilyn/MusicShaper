class MusicNote {
    /**
     * @param {Tone.Monophonic & { notesColor: string; name: string; }} instrument
     * @param {number} pos
     * @param {number} duration
     * @param {number} noteId
     * @param {number} octave
     */
    constructor(instrument, pos, duration, noteId, octave) {
        this.instrument = instrument;
        this.time = pos;
        this.length = duration;
        this.notation = noteId;
        this.octave = octave;
    }

    remove() {
        const index = musicNotes.findIndex(n => n == this);
        musicNotes.splice(index, 1);
        stop();
    }

    /**
     * @returns {boolean}
     */
    checkIntersections() {
        const related_notes = musicNotes.filter(
            n => this.octave == n.octave && this.notation == n.notation && this.time < n.time
        );
        return related_notes.some(n => this.time + this.length > n.time);
    }

    get instrumentName() {
        return this.instrument.name;
    }

    get duration() {
        return new Tone.Time('16n').toSeconds() * this.length;
    }

    get noteNotation() {
        return noteNotations[this.notation - 1] + this.octave;
    }

    playPreview(time = undefined) {
        console.log(this.notation);
        let args;
        if (this.instrument instanceof Tone.PolySynth) {
            args = [[this.noteNotation], this.duration, time];
        }
        if (this.instrument instanceof Tone.NoiseSynth) {
            args = [this.duration, time];
        }
        else {
            args = [this.noteNotation, this.duration, time];
        }
        this.instrument.triggerAttackRelease.apply(this.instrument, args);
    }

    /**
     * @param {MusicNote} note
     */
    static place(note) {
        musicNotes.push(note);
        return note;
    }

    /**
     * @param {paper.Path.Rectangle} path
     * @param {paper.Size} cellSize
     */
    static makeNoteFromPath(path, cellSize) {
        const coordY = Math.floor(path.bounds.top / cellSize.height);
        return new MusicNote(
            currentInstrument,
            Math.floor(path.bounds.left / cellSize.width),
            Math.floor(path.bounds.width / cellSize.width),
            noteNotations.length - coordY % noteNotations.length,
            octavesFrom + octaves - Math.floor(coordY / noteNotations.length) - 1
        );
    }
}



/** @type {MusicNote[]} */
var musicNotes = JSON.parse(document.getElementById('musicNotes').innerText)
    .map(n => new MusicNote(
        Object.values(instruments).find(i => i.id == n.instrument),
        n.time,
        n.length,
        n.notation,
        n.octave,
    ));
