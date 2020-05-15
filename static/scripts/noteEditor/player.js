function groupBy(xs, key) {
    return xs.reduce(function(rv, x) {
        (rv[x[key]] = rv[x[key]] || []).push(x);
        return rv;
    }, {});
};

var isPlaying = false;

function stop() {
    isPlaying = false;
    hidePlayhead();
    Tone.Transport.stop();
    Tone.Transport.cancel(0);
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

    if (musicNotes.length == 0) {
        return;
    }

    function scheduleDraw(timeX, sTime) {
        Tone.Draw.schedule(() => {
            movePlayheadTo(timeX);
        }, sTime);
    }

    const sixteenthSec = new Tone.Time('16n').toSeconds();

    const timedNotes = groupBy(musicNotes, 'time');
    let lastTime = Math.max(...Object.keys(timedNotes).map(Number));
    for (let time = 0; time <= lastTime; time++) {
        if (time < from) continue;

        const toneTime = sixteenthSec * (time - from);
        const notes = timedNotes[time];
        if (!notes) {
            Tone.Transport.scheduleOnce(sTime => {
                scheduleDraw(time, sTime);
            }, toneTime);
            continue;
        }

        const groupedByInstr = groupBy(notes, 'instrumentName');
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
                    scheduleDraw(time, sTime);
                }, toneTime);
            }
            else {
                Tone.Transport.scheduleOnce(sTime => {
                    relatedNotes.forEach(n => n.playPreview(sTime));
                    scheduleDraw(sTime);
                }, toneTime);
            }
        }
    }

    const lastNoteLength = Math.max(...timedNotes[lastTime].map(n => n.length));
    for (let timeX = 0; timeX < lastNoteLength; timeX++) {
        Tone.Transport.scheduleOnce(sTime => {
            scheduleDraw(lastTime + timeX, sTime);
        }, sixteenthSec * (lastTime + timeX - from));
    }

    Tone.Transport.scheduleOnce(() => {
        hidePlayhead();
        isPlaying = false;
    }, sixteenthSec * (lastTime + lastNoteLength + 1 - from));

    Tone.Transport.scheduleOnce(() => {
        movePlayheadTo(from);
        showPlayhead();
        isPlaying = true;
    }, 0);

    Tone.Transport.start('+0.1');
}

document.onkeydown = function ({ keyCode, repeat }) {
    if (!repeat && keyCode == 32) {
        if (isPlaying) {
            stop();
        }
        else {
            play(0);
        }
        return false;
    }
}
