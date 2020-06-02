/// <reference path="../libs/@types/Tone.d.ts" />
/// <reference path="noteEditor/musicNote.js" />

/**
 * @typedef {{ name: string; duration: number; color: string; }} Pattern
 */

class PatternStorage {
    /**
     * @param {Record<string, Pattern>} patternsDataMap
     * @param {InstrumentStorage} instruments
     */
    constructor(patternsDataMap, instruments) {
        /** @type {Map<string, Pattern & { part: Tone.Part }>} */
        this.patterns = new Map();

        for (const name in patternsDataMap) {
            const p = patternsDataMap[name];
            Object.defineProperty(p, 'part', {
                get: () => PatternStorage.patternToTonePart(p, instruments)
            });
            this.patterns.set(name, p);
        }

        this.selectPattern(this.patterns.keys().next().value);
    }

    /**
     * @param {string} name
     * @returns {Pattern}
     */
    selectPattern(name) {
        if (!this.patterns.has(name)) return;
        const oldPattern = this.current;
        this.current = this.patterns.get(name);
        window.dispatchEvent(new CustomEvent('patternSelected', {
            detail: { oldPattern, current: this.current }
        }));
        return this.current;
    }

    /**
     * @returns {Pattern}
     */
    get firstPattern() {
        return this.patterns.values().next().value;
    }

    /**
     * @param {Pattern} patternData
     * @param {InstrumentStorage} instruments
     * @returns {Pattern & Tone.Part}
     */
    static patternToTonePart(patternData, instruments) {
        const events = [];

        const timedNotes = groupBy(patternData.notes, 'time');

        const sixteenthSec = new Tone.TransportTime('16n').toSeconds();

        for (const time in timedNotes) {
            const notes = timedNotes[time];
            const instrNotesData = groupBy(notes, 'instrument');

            for (const instrId in instrNotesData) {
                const event = {time: sixteenthSec * time};

                const instr = instruments.getById(instrId);

                const instrNotes = instrNotesData[instrId].map(data => new MusicNote(
                    instr, data.time, data, data.length
                ));

                if (instr instanceof Tone.PolySynth) {
                    Object.assign(event, {
                        poly: true,
                        instr,
                        durations: instrNotes.map(n => n.duration),
                        notations: instrNotes.map(n => n.letterNotation),
                    });
                }
                else {
                    Object.assign(event, {
                        notes: instrNotes
                    });
                }

                events.push(event);
            }
        }

        const part = new Tone.Part((sTime, event) => {
            if (event.poly) event.instr.triggerAttackRelease(event.notations, event.durations, sTime);
            else event.notes.forEach(n => n.playPreview(sTime));
        }, events);

        return Object.assign(part, patternData);
    }
}