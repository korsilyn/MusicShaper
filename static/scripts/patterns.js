/// <reference path="../libs/@types/Tone.d.ts" />
/// <reference path="noteEditor/musicNote.js" />

/**
 * @typedef {Tone.Part & { name: string; duration: number; color: string; }} Pattern
 */

class PatternStorage {

    static sixteenthSec = new Tone.Time('16n').toSeconds();

    /**
     * @param {Record<string, Pattern>} patternsDataMap
     * @param {InstrumentStorage} instruments
     */
    constructor(patternsDataMap, instruments) {
        /** @type {Map<string, Tone.Part>} */
        this.parts = new Map();

        for (const name in patternsDataMap) {
            this.parts.set(name, PatternStorage.patternToTonePart(
                patternsDataMap[name], instruments
            ));
        }

        this.selectPattern(this.parts.keys().next().value);
    }

    /**
     * @param {string} name
     * @returns {Pattern}
     */
    selectPattern(name) {
        if (!this.parts.has(name)) return;
        const oldPattern = this.current;
        this.current = this.parts.get(name);
        window.dispatchEvent(new CustomEvent('patternSelected', {
            detail: { oldPattern, current: this.current }
        }));
        return this.current;
    }

    /**
     * @returns {Pattern}
     */
    get firstPattern() {
        return this.parts.values().next().value;
    }

    /**
     * @param {Pattern} patternData
     * @param {InstrumentStorage} instruments
     * @returns {Tone.Part}
     */
    static patternToTonePart(patternData, instruments) {
        const events = [];

        const timedNotes = groupBy(patternData.notes, 'time');

        for (let time = 0; time < patternData.duration; time++) {
            const notes = timedNotes[time];
            if (!notes) continue;
            const instrNotesData = groupBy(notes, 'instrument');

            const event = [PatternStorage.sixteenthSec * time];
            for (const instrId in instrNotesData) {
                const instr = instruments.getById(instrId);

                const instrNotes = instrNotesData[instrId].map(data => new MusicNote(
                    instr, data.time, data, data.length
                ));

                if (instr instanceof Tone.PolySynth) {
                    event.push({
                        poly: true, instr,
                        durations: instrNotes.map(n => n.duration),
                        notations: instrNotes.map(n => n.letterNotation),
                    });
                }
                else {
                    event.push({
                        poly: false,
                        instr,
                        notes: instrNotes
                    });
                }
            }

            events.push(event);
        }

        const part = new Tone.Part((sTime, event) => {
            if (event.poly) {
                event.instr.triggerAttackRelease(event.notations, event.durations, sTime);
            }
            else {
                event.notes.forEach(n => n.playPreview(sTime));
            }
        }, events);

        delete patternData['notes'];

        return {
            ...part,
            ...patternData,
        }
    }
}