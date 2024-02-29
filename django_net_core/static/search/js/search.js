"use strict";


function main() {
    setSearchListener();
}


function setSearchListener() {
    let formTag = document.getElementById('search_form');
    let inputTag = formTag.querySelector('#search');

    formTag.addEventListener('submit', (event) => {
        if (inputTag.value.trim() === '') event.preventDefault();
    });
}


document.addEventListener("DOMContentLoaded", main);