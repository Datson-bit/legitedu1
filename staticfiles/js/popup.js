// static/js/popup.js
document.addEventListener('DOMContentLoaded', function() {
    var popup = document.getElementById('ad-popup');
    var closeButton = document.getElementById('close-popup');

    if (popup) {
        setTimeout(function() {
            popup.style.display = 'block';
        }, 3000);  // Show the popup after 3 seconds

        closeButton.addEventListener('click', function() {
            popup.style.display = 'none';
        });
    }
});
