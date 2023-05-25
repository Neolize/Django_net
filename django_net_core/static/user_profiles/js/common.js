"use strict";

// inputMask

function main() {
    initiateInputMask();

    selectGender();

    changeBirthdayFieldClass();
}


function initiateInputMask() {
    let phoneInput = document.getElementById('form-edit__phone');
    let inputMask = new Inputmask('+7 (999) 999-99-99');
    inputMask.mask(phoneInput); 
}


function selectGender() {
    let tagSelect = document.getElementById('form-edit__gender');
    let options = tagSelect.querySelectorAll('option');
    let gender = tagSelect.dataset.gender;

    for (let option of options) {
        if (option.value === gender) {
            option.selected = true;
        }
    }
}


function changeBirthdayFieldClass() {
    if (document.getElementById('form-edit__disabled-birthday')) {
        let birthdayField = document.getElementById('form-edit__birthday');
        birthdayField.classList.add('profile-form__birthday');
    }
}


document.addEventListener('DOMContentLoaded', main);