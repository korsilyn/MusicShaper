/**
 * @returns {string[]}
 */
function getNoteNames() {
    return ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
}

/**
 * @param {number} from
 * @param {number} to
 * @returns {string[]}
 */
function getNotes(from = 2, to = 7) {
    const noteNames = getNoteNames();
    const notes = [];

    let i;

    const makeNotes = () => {
        for (const noteName of noteNames) {
            notes.push(noteName + i);
        }
    }

    if (from > to) {
        for (i = from; i >= to; i--) {
            makeNotes();
        }
    }
    else {
        for (i = from; i <= to; i++) {
            makeNotes();
        }
    }

    return notes;
}
