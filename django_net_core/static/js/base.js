"use strict";


function main() {
    setCurrentYear();
    activateHeaderButtons();
}


function setCurrentYear() {
    let container = document.getElementById('footer-year');
    let currentYear = new Date().getFullYear();
    container.innerHTML = currentYear;
}


function activateHeaderButtons() {
    searchSigninButton();
    searchSignupButton();
}


function searchSigninButton() {
    let signinButton = document.getElementById('signin-header-button');
    if (signinButton) {
        signinButton.addEventListener('click', (event) => {
            let signinLink = event.target.querySelector('a');
            signinLink.click();
        });
    }
}


function searchSignupButton() {
    let signupButton = document.getElementById('signup-header-button');
    signupButton.addEventListener('click', (event) => {
        let signupLink = event.target.querySelector('a');
        signupLink.click();
    });
}


document.addEventListener("DOMContentLoaded", main);