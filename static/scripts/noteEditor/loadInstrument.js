/// <reference path="../../libs/@types/Tone.d.ts" />

function requestInstrument(instrumentName) {
    return new Promise((resolve, reject) => {
        $.ajax({
            method: 'GET',
            dataType: 'json',
            url: window.location.href,
            data: {
                csrfmiddlewaretoken: '{{ csrf_token }}',
                operation: 'loadInstrument',
                instrumentName,
            },
            success: (data) => {
                if (data.success && data[instrumentName]) {
                    resolve(data[instrumentName]);
                }
                else {
                    reject('failed');
                }
            },
            error: (e, s, thrownErr) => {
                reject(thrownErr);
            }
        })
    });
}

/**
 * @param {{}} settings 
 * @returns {Tone.Instrument & { notesColor: string }}
 */
function makeSynth(settings, name = undefined) {
    const constr = Tone[settings._type || ""];
    if (typeof constr != 'function') {
        throw new Error('invalid instrument');
    }

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

/** @param {string} name */
async function loadInstrument(name) {
    try {
        canvas.style.visibility = 'hidden';
        document.body.style.cursor = 'wait';
        if (!instruments[name]) {
            instruments[name] = makeSynth(await requestInstrument(name));
            instruments[name].name = name;
        }
        canvas.style.visibility = 'visible';
        document.body.style.cursor = null;
        return instruments[name];
    }
    catch (err) {
        console.error(`failed to request instrument: ${err}`);
    }
}

var allInstrumentNames = JSON.parse(document.getElementById('allInstrumentNames').innerText);

var instruments = JSON.parse(document.getElementById('usedInstruments').innerText);
for (const name in instruments) {
    instruments[name] = makeSynth(instruments[name], name);
}
