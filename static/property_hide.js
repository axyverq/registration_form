function changeClassPropertyHide() {
    var elements = document.getElementsByClassName("error");
    
    for (var i = 0; i < elements.length; i++) {
        if (!elements[i].querySelector("#displaying")) {
            elements[i].style.display = "none";
        }
        console.log(`Element ${i} has content: "${elements[i].textContent}"`);
    }
}
