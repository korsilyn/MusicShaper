function groupBy(xs, key) {
    return xs.reduce(function(rv, x) {
        (rv[x[key]] = rv[x[key]] || []).push(x);
        return rv;
    }, {});
};

function stop() {
    Tone.Transport.stop();
    Tone.Transport.clear(0);
    Object.values(instruments).forEach(i => {
        if (i instanceof Tone.PolySynth) {
            i.releaseAll(0);
        }
        else if (i instanceof Tone.Monophonic) {
            i.triggerRelease(0);
        }
    });
}

function play(from = 0) {
    stop();

    const timedNotes = groupBy(musicNotes, 'time');
    for (const time in timedNotes) {
        if (time < from) continue;

        const notes = timedNotes[time];
        const groupedByInstr = groupBy(notes, 'instrumentName');

        const toneTime = new Tone.Time('16n').toSeconds() * time;

        const processed = [];

        for (const instrName in groupedByInstr) {
            if (processed.includes(instrName)) continue;
            processed.push(instrName);
            const instr = instruments[instrName];
            const relatedNotes = notes.filter(n => n.instrumentName == instrName);
            if (instr instanceof Tone.PolySynth) {
                Tone.Transport.scheduleOnce(sTime => {
                    instr.triggerAttackRelease(
                        relatedNotes.map(n => n.noteNotation),
                        relatedNotes.map(n => n.duration),
                        sTime
                    );
                }, toneTime);
            }
            else {
                Tone.Transport.scheduleOnce(sTime => {
                    relatedNotes.forEach(n => n.playPreview(sTime));
                }, toneTime);
            }
        }
    }

    Tone.Transport.start('+4i');
}
