function changeClassProperty() {
    var elements = document.getElementsByClassName("displaying");
    
    for (var i = 0; i < elements.length; i++) {
        if (elements[i].textContent.trim() !== "") {
            elements[i].style.display = "inline";
        }
    }
}
