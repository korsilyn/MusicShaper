/// <reference path="../../libs/@types/Tone.d.ts" />

class Recorder {
    /**
     * @param {string} recordBtnQuery
     */
    constructor(recordBtnQuery) {
        this.recordBtn = document.querySelector(recordBtnQuery);

        this.recording = false;

        this.recordingBlob = null;

        window.addEventListener('stop', ({ detail: { reason } }) => {
            if (!this.recording || reason == 'beforePlay') return;
            this.mediaRecorder.stop();
            this.recording = false;
        });

        this.recordBtn.addEventListener('click', () => {
            player.play();
            this.start();
        });

        const checkDuration = () => {
            if (window.calculateDuration() == 0) {
                this.recordBtn.disabled = true;
            }
        }

        window.addEventListener('tileEditorInit', checkDuration);
        window.addEventListener('tilePlaced', () => this.recordBtn.disabled = false);
        window.addEventListener('tileRemoved', checkDuration);
    }

    get context() {
        return Tone.context;
    }

    get streamDest() {
        return this.context.createMediaStreamDestination();
    }

    start() {
        const dest = this.streamDest;
        const chunks = [];

        this.mediaRecorder = new MediaRecorder(dest.stream);

        for (const i of instruments.instruments.values()) {
            i.connect(dest);
        }

        this.mediaRecorder.ondataavailable = event => {
            chunks.push(event.data);
        };

        this.mediaRecorder.onstop = () => {
            this.recordingBlob = new Blob(chunks, {
                type: 'audio/ogg; codecs=opus',
            });

            for (const i of instruments.instruments.values()) {
                i.disconnect(dest);
            }

            window.dispatchEvent(new CustomEvent('recorded', {
                detail: { blob: this.recordingBlob }
            }));
        };

        this.mediaRecorder.start();
        this.recording = true;
    }
}