function save() {
    let notes = Tile.tiles.map(tile => tile.note.json);
    if (notes.length == 0) {
        notes = [''];
    }

    return new Promise((resolve, reject) => $.ajax({
        method: 'POST',
        dataType: 'json',
        url: Urls.reverseUrl('save_pattern'),
        data: {
            csrfmiddlewaretoken: csrf_token,
            'notes[]': notes,
            'bpm': bpmInput.safeValue,
        },

        success: data => {
            if (data.success) {
                resolve();
            }
            else {
                reject('failed');
            }
        },

        error: (x, e, thrownError) => {
            reject(thrownError);
        },
    }))
}

document.querySelector('button.saveBtn').onclick = function () {
    this.classList.add('btn-outline-dark');
    this.disabled = true;
    save()
        .finally(() => {
            this.classList.remove('btn-outline-dark');
            this.disabled = false;
        })
        .catch(() => alert('Произошла ошибка. Повторите попытку позже'));
};

window.addEventListener('beforeunload', e => {
    const returnValue = 'Несохранённые изменения будут утеряны';
    e.returnValue = returnValue;
    return returnValue;
});
