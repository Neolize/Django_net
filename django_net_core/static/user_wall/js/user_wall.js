"use strict";


function main() {
    modifyChildComments();
    modifyErrorBlock();
}


function modifyChildComments() {
    // The function adds links to a users' pages if their comments were replied.
    const childComments = document.querySelectorAll('[data-child-comment]');
    const regexp = /(,\s{1})/g;

    for (const child of childComments) {
        const parent = document.querySelector(`[data-parent-comment-pk="${child.dataset.childComment}"]`);
        const parentURL = parent.dataset.parentCommentUrl;

        const found = child.innerHTML.search(regexp);
        const linkToParentComment = createLinkToParentComment(child.innerHTML.slice(0, found), parentURL);
        child.innerHTML = child.innerHTML.slice(found);
        child.insertAdjacentElement('afterbegin', linkToParentComment);
    }
}


function createLinkToParentComment(content, link) {
    const newLink = document.createElement('a');
    newLink.innerHTML = content;
    newLink.href = link;
    newLink.target = '_blank';
    return newLink;
}


function modifyErrorBlock() {
    adjustErrorList();
    const errors = document.querySelectorAll('[data-error]');
    for (const error of errors) {
        const newElement = createElementToCloseError();
        error.insertAdjacentElement('afterbegin', newElement);
        newElement.addEventListener('click', closeErrorBlock);
        adjustErrorBlock(error);
    }
}


function adjustErrorList() {
    const allErrors = document.querySelectorAll('.errorlist');
    for (const error of allErrors) {
        error.style.listStyle = 'none';
        error.style.position = 'relative';
        error.style.bottom = '23px';
        error.style.paddingLeft = '0px';
        error.style.marginLeft = '30px';
    }
}


function adjustErrorBlock(errorBlock) {
    const errorRect = errorBlock.getBoundingClientRect();
    errorBlock.style.height = `${errorRect.height - 23}px`;
}


function createElementToCloseError() {
    const newElement = document.createElement('block');
    newElement.className = 'close_error_block';
    return newElement;
}


function closeErrorBlock() {
    const input = document.getElementById('input_error');
    const form = document.getElementById('formComment');
    input.value = 'closed';
    form.submit();
}


document.addEventListener('DOMContentLoaded', main);