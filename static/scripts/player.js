/// <reference path="instruments.js" />

class Player {
    /**
     * @param {string} playBtnQuery
     * @param {string} stopBtnQuery
     * @param {string} loopBtnQuery
     */
    constructor(playBtnQuery, stopBtnQuery, loopBtnQuery) {
        this.isPlaying = false;
        this.isLoop = false;

        this.playBtn = document.querySelector(playBtnQuery);
        this.stopBtn = document.querySelector(stopBtnQuery);
        this.loopBtn = document.querySelector(loopBtnQuery);

        this.loopBtn.onclick = () => {
            this.isLoop = !this.isLoop;
            this.loopBtn.style.setProperty('--img-margin', (this.isLoop ? 5 : 3) + 'px');
        }

        window.addEventListener('stop', () => {
            hidePlayhead();
            this.isPlaying = false;
            this.playBtn.disabled = false;
            this.loopBtn.disabled = false;
            Tone.Transport.stop();
            Tone.Transport.cancel(0);
        });

        this.playBtn.addEventListener('click', () => {
            this.play(0);
        });

        this.stopBtn.addEventListener('click', () => {
            this.stop('user');
        });

        window.addEventListener('keydown', ({ keyCode, repeat }) => {
            if (!repeat && keyCode == 32) {
                if (this.isPlaying) {
                    this.stop('user');
                }
                else {
                    this.play(0);
                }
                return false;
            }
        });

        window.addEventListener('tileEditorMouseUp', ({ detail: { cellPoint, button } }) => {
            if (button == 1) {
                player.play(cellPoint.x);
            }
        });
    }

    stop(reason) {
        window.dispatchEvent(new CustomEvent('stop', {
            detail: { reason }
        }));
    }

    /**
     * @param {number} posX
     * @param {number} sTime
     */
    schedulePlayhead(posX, sTime) {
        return Tone.Draw.schedule(() => {
            movePlayheadTo(posX);
        }, sTime);
    }

    get baseTimeSeconds() {
        return new Tone.TransportTime('16n').toSeconds();
    }

    /**
     * @param {number} from
     * @returns {number} duration
     */
    scheduleEvents(from) {
        throw new Error('not implemented Player.scheduleEvents');
    }

    play(from = 0) {
        this.stop('beforePlay');

        const endTime = this.scheduleEvents(from);
        if (!endTime) return;

        const sixteenthSec = this.baseTimeSeconds;

        Tone.Transport.schedule(() => {
            if (!this.isLoop) {
                this.stop('end');
            }
        }, sixteenthSec * (endTime + 1 - from));

        Tone.Transport.schedule(() => {
            window.movePlayheadTo(from);
            window.showPlayhead();
            this.isPlaying = true;
        }, 0);

        Tone.Transport.start('+0.1');

        Tone.Transport.loop = this.isLoop;
        if (Tone.Transport.loop) {
            Tone.Transport.loopEnd = sixteenthSec * (endTime + 1 - from);
        }

        this.loopBtn.disabled = true;
        this.playBtn.disabled = true;
    }
}
