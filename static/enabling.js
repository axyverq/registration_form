function enableAllButtons() {
    document.querySelectorAll('button[disabled]').forEach(button => {
        button.removeAttribute('disabled');
    });
}
