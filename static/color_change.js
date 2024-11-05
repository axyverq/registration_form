// функция изменения цвета границы input поля
function changeInputBorderColor(id, color) {
    const input = document.getElementById(id);
    if (input) {
        input.style.borderColor = color;
    }
}