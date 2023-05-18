"use strict";


function main() {
    let container = document.getElementById('footer-year');
    let currentYear = new Date().getFullYear();
    container.innerHTML = currentYear;
}


document.addEventListener("DOMContentLoaded", main);