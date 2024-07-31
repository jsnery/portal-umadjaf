document.addEventListener("keydown", function (event) {
    if (event.key === "F12") {
        event.preventDefault();
    }
    if (event.ctrlKey && event.shiftKey && event.key === "I") {
        event.preventDefault();
    }
    if (event.ctrlKey && event.shiftKey && event.key === "J") {
        event.preventDefault();
    }
    if (event.ctrlKey && event.key === "U") {
        event.preventDefault();
    }
});

document.addEventListener("contextmenu", function (event) {
    event.preventDefault();
});