document.addEventListener('DOMContentLoaded', function() {
    let hamburgericon = document.querySelector('#hamburger');
    hamburgericon.addEventListener('click', function() {
        hamburgericon.classList.toggle('open');
    })
    });