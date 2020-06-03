class NotePlayer extends Player {
    /**
     * @param {InstrumentStorage} instruments
     * @param {string} playBtnQuery
     * @param {string} stopBtnQuery
     * @param {string} loopBtnQuery
     */
    constructor(instruments, playBtnQuery, stopBtnQuery, loopBtnQuery) {
        super(playBtnQuery, stopBtnQuery, loopBtnQuery);

        this.instruments = instruments;

        window.addEventListener('stop', () => {
            for (const i of this.instruments.instruments.values()) {
                if (i instanceof Tone.PolySynth) i.releaseAll(0);
                else i.triggerRelease(0);
            }
        });
    }

    scheduleEvents(from) {
        /** @type {MusicNote[]} */
        const musicNotes = Tile.tiles.map(tile => tile.note);

        if (musicNotes.length == 0) return;

        const sixteenthSec = this.baseTimeSeconds;

        const timedNotes = groupBy(musicNotes, 'time');
        const endTime = Math.max(...musicNotes.map(n => n.time + n.length));

        if (from >= endTime) return;

        for (let time = from; time < endTime; time++) {
            const toneTime = sixteenthSec * (time - from);
            const notes = timedNotes[time];
            if (!notes) {
                Tone.Transport.schedule(sTime => {
                    this.schedulePlayhead(time, sTime);
                }, toneTime);
                continue;
            }

            const groupedByInstr = groupBy(notes, 'instrumentName');

            for (const instrName in groupedByInstr) {
                const instr = this.instruments.getByName(instrName);
                if (instr instanceof Tone.PolySynth) {
                    Tone.Transport.schedule(sTime => {
                        instr.triggerAttackRelease(
                            groupedByInstr[instrName].map(n => n.letterNotation),
                            groupedByInstr[instrName].map(n => n.duration),
                            sTime
                        );
                        this.schedulePlayhead(time, sTime);
                    }, toneTime);
                }
                else {
                    Tone.Transport.schedule(sTime => {
                        groupedByInstr[instrName].forEach(n => n.playPreview(sTime));
                        this.schedulePlayhead(time, sTime);
                    }, toneTime);
                }
            }
        }

        return endTime;
    }
}