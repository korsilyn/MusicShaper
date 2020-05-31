/// <reference path="../libs/@types/Tone.d.ts" />

class InstrumentStorage {
    /**
     * @typedef {Tone.Instrument & { id: number; notesColor: string; name: string; }} Instrument
     */

    /**
     * @param {Record<string, {}>} instrumentSettings
     * @param {string[]} allInstrumentNames
     */
    constructor(instrumentSettings, allInstrumentNames) {
        /** @type {Map<string, Instrument>} */
        this.instruments = new Map();

        for (const name in instrumentSettings) {
            this.instruments.set(name, InstrumentStorage.makeSynth(instrumentSettings[name], name));
        }

        /** @type {Instrument} */
        this.current;
        this.loadCurrentInstrument(this.firstInstrument ? this.firstInstrument.name : allInstrumentNames[0]);
    }

    get instrumentNames() {
        return [...this.instruments.keys()];
    }

    /**
     * @param {string} name
     */
    getByName(name) {
        return this.instruments.get(name);
    }

    /**
     * @param {number} id
     */
    getById(id) {
        for (const i of this.instruments.values()) {
            if (i.id == id) return i;
        }
    }

    /**
     * @returns {Instrument}
     */
    get firstInstrument() {
        return this.instruments.values().next().value;
    }

    /**
     * @param {string} name
     */
    static requestInstrument(name) {
        return new Promise((resolve, reject) => {
            $.ajax({
                method: 'GET',
                dataType: 'json',
                url: Urls.reverseUrl('get_instrument'),
                data: {
                    csrfmiddlewaretoken: csrf_token,
                    name,
                },
                success: data => {
                    if (data[name])
                        resolve(data[name]);
                    else
                        reject('failed');
                },
                error: (e, s, thrownErr) => {
                    reject(thrownErr);
                }
            })
        });
    }

    /**
     * @param {{}} settings
     * @param {string} name
     * @returns {Instrument}
     */
    static makeSynth(settings, name = undefined) {
        const constr = Tone[settings._type || ""];
        if (typeof constr != 'function') {
            throw new Error('invalid instrument');
        }

        /** @type {Tone.Instrument} */
        let synth;
        if (constr.prototype instanceof Tone.Monophonic) {
            synth = new Tone.PolySynth(noteNotationsTotalLenght, constr);
            synth.set(settings);
        }
        else {
            synth = new constr(settings);
        }

        synth.toMaster();

        synth.notesColor = settings._notesColor;
        synth.id = settings._id;
        synth.name = name;

        return synth;
    }

    /**
     * @param {string} name
     * @returns {Promise<Instrument>}
     */
    async loadInstrument(name) {
        try {
            window.dispatchEvent(new Event('beforeInstrumentLoad'));
            let i = this.instruments.get(name);
            if (i === undefined) {
                i = InstrumentStorage.makeSynth(await InstrumentStorage.requestInstrument(name));
                i.name = name;
                this.instruments.set(name, i);
            }
            window.dispatchEvent(new CustomEvent('instrumentLoad', {
                detail: i
            }));
            return i;
        }
        catch (err) {
            console.error(`failed to request instrument: ${err}`);
        }
        return null;
    }

    /**
     * @param {string} name
     */
    async loadCurrentInstrument(name) {
        const instr = await this.loadInstrument(name);
        if (instr) {
            this.current = instr;
            window.dispatchEvent(new Event('instrumentSelected'));
        }
    }
}
