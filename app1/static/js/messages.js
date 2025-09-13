document.addEventListener("DOMContentLoaded", function() {
    const popup = document.getElementById("popup-message");
    if (popup) {
        setTimeout(() => {
            popup.remove();
        }, 3000); // matches animation duration
    }
});

