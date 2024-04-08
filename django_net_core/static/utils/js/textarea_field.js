"use strict";


function main() {
    addEventToTextarea();
}


function addEventToTextarea() {
    const textarea = document.getElementById('form-edit__info_about_user');
    textarea.addEventListener('keyup', validateTextarea);
    textarea.addEventListener('focus', validateTextarea);
}


function validateTextarea(event) {
    const textarea = event.target;
    const maxLength = textarea.dataset.maxLength;
    const textLength = textarea.value.length;
    const textCount = document.getElementById('text_count');
    const wordCount = document.getElementById('words_count');
    textCount.innerHTML = textLength;
    
    if(textLength > maxLength){
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