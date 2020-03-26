/**
 * @returns {string[]}
 */
function getNoteNames() {
    return ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
}

/**
 * @param {number} from
 * @param {number} to
 * @returns {string[]}
 */
function getNotes(from=2, to=7) {
    const noteNames = getNoteNames();
    const notes = [];

    for (let i = from; i <= to; i++) {
        for (const noteName of noteNames) {
            notes.push(noteName + i);
        }
    }
    
    return notes;
}
