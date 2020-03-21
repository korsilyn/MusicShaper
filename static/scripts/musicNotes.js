/**
 * @param {number} from
 * @param {number} to
 * @returns {string[]}
 */
function getMusicNotes(from=2, to=8) {
    const noteNames = ['C', 'D', '_E', 'F', 'G', 'A', '_B'];
    const notes = [];

    for (let i = to; i >= from; i--) {
        for (const noteName of noteNames) {
            const noteSafe = noteName.replace('_', '');
            if (!noteName.startsWith('_')) {
                notes.push(noteSafe + '#' + i);
            }
            notes.push(noteSafe + i);
        }
    }
    
    return notes;
}
