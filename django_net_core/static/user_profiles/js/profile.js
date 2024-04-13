"use strict";


function main() {
    scrollToPosts();
}


function addChildReview(name, parent_id) {
    let userCommentInput = document.getElementById('usercomment-input');
    userCommentInput.innerHTML = `${name}, `;
    userCommentInput.setSelectionRange(userCommentInput.value.length, userCommentInput.value.length, 'forward');

    document.getElementById('parentcomment').value = parent_id;
}


function scrollToPosts() {
    const postElements = document.querySelectorAll('.posts_number');
    for (const postElement of postElements) {
        if (postElement) {
            const userPostItem = document.getElementById('user-post-item');
    
            const userPostRect = userPostItem.getBoundingClientRect();
            const bodyRect = document.body.getBoundingClientRect();
            
            postElement.addEventListener('click', () => {
                window.scrollTo(0, userPostRect.y - bodyRect.y);
            });
        }
    }
}


document.addEventListener('DOMContentLoaded', main);