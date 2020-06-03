class TimelinePlayer extends Player {
    /**
     * @param {PatternStorage} patterns
     * @param {string} playBtnQuery
     * @param {string} stopBtnQuery
     * @param {string} loopBtnQuery
     */
    constructor(patterns, playBtnQuery, stopBtnQuery, loopBtnQuery) {
        super(playBtnQuery, stopBtnQuery, loopBtnQuery);
        this.patterns = patterns;

        window.addEventListener('stop', () => {
            Tile.tiles.forEach(tile => {
                if (tile.cached_part)
                    try {
                        tile.cached_part.dispose();
                    }
                    catch { }
            });
        });
    }

    scheduleEvents(from) {
        const duration = window.calculateDuration();

        /** @type {(Pattern & { time: number; })[]} */
        const parts = Tile.tiles.map(tile => {
            const part = tile.pattern.part;
            part.time = tile.x;
            tile.cached_part = part;
            return part;
        });

        /** @type {{ [time: number]: Pattern[] }} */
        const timedParts = groupBy(parts, 'time');

        const baseTime = this.baseTimeSeconds;

        if (from > 0) {
            const inheadParts = parts.filter(p => p.time < from && p.time + p.duration >= from);;
            inheadParts.forEach(part => part.start(0, (from - part.time) * baseTime));
        }

        for (let time = from; time < duration; time++) {
            const toneTime = baseTime * (time - from);
            Tone.Transport.schedule(sTime => {
                this.schedulePlayhead(time, sTime);
            }, toneTime);
            if (timedParts[time]) {
                timedParts[time].forEach(part => part.start(toneTime));
            }
        }

        return duration;
    }
}