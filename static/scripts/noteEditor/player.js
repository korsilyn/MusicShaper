/** @type {HTMLButtonElement} */
const playBtn = document.querySelector('button.playBtn');
/** @type {HTMLButtonElement} */
const stopBtn = document.querySelector('button.stopBtn');

/** @type {HTMLInputElement} */
const loopToggleBtn = document.querySelector('button.loopBtn');

var isPlaying = false;
var isLoop = false;

loopToggleBtn.onclick = function () {
    isLoop = !isLoop;
    this.style.setProperty('--img-margin', (isLoop ? 5 : 3) + 'px');
}

function stop() {
    if (isPlaying) {
        window.dispatchEvent(new Event('stop'));
    }
}

function play(from = 0) {
    stop();

    /** @type {MusicNote[]} */
    const musicNotes = Tile.tiles.map(tile => tile.note);

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
    const lastTime = Math.max(...musicNotes.map(n => n.time + n.length));

    if (from >= lastTime) {
        return;
    }

    for (let time = 0; time < lastTime; time++) {
        if (time < from) continue;

        const toneTime = sixteenthSec * (time - from);
        const notes = timedNotes[time];
        if (!notes) {
            Tone.Transport.schedule(sTime => {
                scheduleDraw(time, sTime);
            }, toneTime);
            continue;
        }

        const groupedByInstr = groupBy(notes, 'instrumentName');
        const processed = [];

        for (const instrName in groupedByInstr) {
            if (processed.includes(instrName)) continue;
            processed.push(instrName);
            const instr = instruments.getByName(instrName);
            if (instr instanceof Tone.PolySynth) {
                Tone.Transport.schedule(sTime => {
                    instr.triggerAttackRelease(
                        groupedByInstr[instrName].map(n => n.letterNotation),
                        groupedByInstr[instrName].map(n => n.duration),
                        sTime
                    );
                    scheduleDraw(time, sTime);
                }, toneTime);
            }
            else {
                Tone.Transport.schedule(sTime => {
                    groupedByInstr[instrName].forEach(n => n.playPreview(sTime));
                    scheduleDraw(time, sTime);
                }, toneTime);
            }
        }
    }

    Tone.Transport.schedule(() => {
        if (!isLoop) {
            stop();
        }
    }, sixteenthSec * (lastTime + 1 - from));

    Tone.Transport.schedule(() => {
        movePlayheadTo(from);
        showPlayhead();
        isPlaying = true;
    }, 0);

    Tone.Transport.start('+0.1');

    Tone.Transport.loop = isLoop;
    if (Tone.Transport.loop) {
        Tone.Transport.loopEnd = sixteenthSec * (lastTime + 1 - from);
    }

    loopToggleBtn.disabled = true;
    playBtn.disabled = true;
}

window.addEventListener('stop', () => {
    hidePlayhead();
    isPlaying = false;
    loopToggleBtn.disabled = false;
    playBtn.disabled = false;
    Tone.Transport.stop();
    Tone.Transport.cancel(0);
    for (const i of instruments.instruments.values()) {
        if (i instanceof Tone.PolySynth) {
            i.releaseAll(0);
        }
        else if (i instanceof Tone.Monophonic) {
            i.triggerRelease(0);
        }
    }
});

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

playBtn.onclick = function () {
    play(0);
}

stopBtn.onclick = function () {
    stop();
}
