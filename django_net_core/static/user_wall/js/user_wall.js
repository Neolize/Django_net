"use strict";


function main() {
    modifyChildComment();
}


function modifyChildComment() {
    const childComment = document.querySelector('.childcomment_block>div.timeline-header>p.usercomment_content');
    const parentElement = document.querySelector('[data-parent-comment]');
    const parentURL = parentElement.dataset.parentComment;

    const regexp = /(,\s{1})/g;
    const found = childComment.innerHTML.search(regexp);

    const linkToParentComment = createLinkToParentComment(childComment.innerHTML.slice(0, found), parentURL);
    childComment.innerHTML = childComment.innerHTML.slice(found);
    childComment.insertAdjacentElement('afterbegin', linkToParentComment);

}


function createLinkToParentComment(content, link) {
    const newLink = document.createElement('a');
    newLink.innerHTML = content;
    newLink.href = link;
    return newLink;
}


document.addEventListener('DOMContentLoaded', main);