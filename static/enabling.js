// функция для изменения доступа к кнопке
function btnsAccess(action) {
    const buttons = document.querySelectorAll('button');
    
    if (action === '+') {
        buttons.forEach(button => {
            button.removeAttribute('disabled');
        });
    } else if (action === '-') {
        buttons.forEach(button => {
            button.setAttribute('disabled', 'true');
        });
    }
}
