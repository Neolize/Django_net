"use strict";


function main() {
    modifyChildComments();
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


document.addEventListener('DOMContentLoaded', main);