let editingCell = null;

document.querySelectorAll('.editable-cell').forEach(cell => {
    const charCode = cell.dataset.charCode;
    const oldValue = parseFloat(cell.dataset.oldValue);

    cell.addEventListener('click', () => {
        if (editingCell && editingCell !== cell) {
            const oldVal = parseFloat(editingCell.dataset.oldValue);
            editingCell.innerText = oldVal.toFixed(4);
            editingCell.contentEditable = false;
        }

        editingCell = cell;
        cell.contentEditable = true;
        cell.focus();
        const range = document.createRange();
        range.selectNodeContents(cell);
        range.collapse(false);
        const sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
    });

    cell.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            if (editingCell === cell) save(cell, charCode);
        } else if (e.key === 'Escape') {
            e.preventDefault();
            if (editingCell === cell) cancel(cell, oldValue);
        }
    });
});

function save(cell, charCode) {
    const raw = cell.innerText.trim();
    let newValue;
    try {
        newValue = parseFloat(raw);
        if (isNaN(newValue) || newValue <= 0) throw new Error();
    } catch (e) {
        alert('Курс должен быть положительным числом');
        cancel(cell, parseFloat(cell.dataset.oldValue));
        return;
    }

    fetch(`/currency/update?${encodeURIComponent(charCode)}=${encodeURIComponent(newValue)}`)
        .then(r => r.ok ? Promise.resolve() : Promise.reject())
        .then(() => {
            cell.dataset.oldValue = newValue;
            cell.innerText = newValue.toFixed(4);
            cell.contentEditable = false;
            cell.blur();
            editingCell = null;
        })
        .catch(() => {
            alert('Не удалось обновить курс');
            cancel(cell, parseFloat(cell.dataset.oldValue));
        });
}

function cancel(cell, oldValue) {
    cell.innerText = oldValue.toFixed(4);
    cell.contentEditable = false;
    cell.blur();
    editingCell = null;
}