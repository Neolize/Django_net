"use strict";


function addChildReview(name, parent_id) {
    let userCommentInput = document.getElementById('usercomment-input');
    userCommentInput.innerHTML = `${name}, `;
    userCommentInput.setSelectionRange(userCommentInput.value.length, userCommentInput.value.length, 'forward');

    document.getElementById('parentcomment').value = parent_id;
}