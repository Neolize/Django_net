"use strict";


function main() {
    const formElement = document.getElementById('post_form');
    formElement.addEventListener('submit', validateTagInput);
}


function validateTagInput() {
    const tagElement = document.getElementById('post_id');
    let tagContent = tagElement.value;
    const regexp = /([a-zA-Z0-9]+[^,;\s]+)/g;

    if(tagContent.trim().length > 0) {

        const matches = [...tagContent.matchAll(regexp)];
        let new_str = '';

        for (const match of matches) {
            if (new_str) {
                new_str = `${new_str}, #${match[0]}`;
            }
            else {
                new_str = `#${match[0]}`;
            }
        }
        tagElement.value = new_str;
    }
}


document.addEventListener('DOMContentLoaded', main);