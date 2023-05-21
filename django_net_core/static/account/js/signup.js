"use strict";


function initiatePasswordIcon() { 
    let passwordIcon = document.getElementById('signup-password-icon');
    passwordIcon.addEventListener('click', handlePasswordIcon);
}


function handlePasswordIcon(event) {
    if (event.target.classList.contains('signup-password-icon__hide')) {
        showPassword(event.target);
    }
    else hidePassword(event.target);
}


function showPassword(passwordIcon) {
    let passwordField = document.getElementById('signup-password-input');
    passwordField.type = 'text';
    passwordIcon.classList.remove('signup-password-icon__hide');
    passwordIcon.classList.add('signup-password-icon__show');
}


function hidePassword(passwordIcon) {
    let passwordField = document.getElementById('signup-password-input');
    passwordField.type = 'password';
    passwordIcon.classList.remove('signup-password-icon__show');
    passwordIcon.classList.add('signup-password-icon__hide');
}


function main() {
    initiatePasswordIcon();
}


document.addEventListener('DOMContentLoaded', main);