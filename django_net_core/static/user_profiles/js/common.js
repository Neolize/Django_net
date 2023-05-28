"use strict";


function main() {
    initiateInputMask();

    selectGender();

    changeBirthdayFieldClass();

    addEventToTextarea();
}


function initiateInputMask() {
    const phoneInput = document.getElementById('form-edit__phone');
    const inputMask = new Inputmask('+7 (999) 999-99-99');
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
        const birthdayField = document.getElementById('form-edit__birthday');
        birthdayField.classList.add('profile-form__birthday');
    }
}


function addEventToTextarea() {
    const textarea = document.getElementById('form-edit__info_about_user');
    textarea.addEventListener('keyup', validateTextarea);
}


function validateTextarea(event) {
    const textarea = event.target;
    const textLength = textarea.value.length;
    const textCount = document.getElementById('text_count');
    const wordCount = document.getElementById('words_count');
    textCount.innerHTML = textLength;
    
    if(textLength > 50){
        textCount.classList.add("text-danger");
        textarea.classList.add("profile-form__textarea_danger");
    }else{
        textCount.classList.remove("text-danger");
        textarea.classList.remove("profile-form__textarea_danger");
    }
     
    if(textLength < 1){
        wordCount.classList.add("d-none");
    }else{
        wordCount.classList.remove("d-none");
    }
}


document.addEventListener('DOMContentLoaded', main);


