"use strict";


function main() {
    scrollToPosts();

    const commentInput = document.getElementById('usercomment-input');
    
    // Changes comment section every time it gets bigger or smaller.
    commentInput.addEventListener('input', changeTextarea);
    commentInput.addEventListener('focus', changeTextarea);

    modifyEditedComments();
}


function addChildReview(event, name, parent_id) {
    event.preventDefault();
    const userCommentInput = document.getElementById('usercomment-input');
    scrollToComment(userCommentInput);

    userCommentInput.value = `${name}, `;
    userCommentInput.setSelectionRange(userCommentInput.value.length, userCommentInput.value.length, 'forward');
    userCommentInput.focus();

    document.getElementById('parentcomment').value = parent_id;
}


function scrollToPosts() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const postsToShow = urlParams.get('posts');

    if(postsToShow) {
        const userPostItem = document.getElementById('user-post-item');
        const userPostRect = userPostItem.getBoundingClientRect();
        const bodyRect = document.body.getBoundingClientRect();

        window.scrollTo(0, userPostRect.y - bodyRect.y);
    }
}


function scrollToComment(commentInput) {
    // scroll to comment input section
    const inputRect = commentInput.getBoundingClientRect();
    const bodyRect = document.body.getBoundingClientRect();

    if (inputRect.y < 5 && inputRect.y > -31) {
        setTimeout( () => {
            window.scrollTo(0, inputRect.y - bodyRect.y - 100);
        }, 2);
    }
    else{
        window.scrollTo(0, (inputRect.y - bodyRect.y - 37));
    }
}


function deletePost(event) {
    const answer = confirm('Are you sure you want to delete this post?');
    if (answer === false) {
        event.preventDefault();
    }
}


function editUserComment(event, commentID, comment) {
    event.preventDefault();
    changeCommentBlockClass();

    const userCommentInput = document.getElementById('usercomment-input');
    const editInput = document.getElementById('editinput');
    const commentIDInput = document.getElementById('comment_id');
    const submitButton = document.getElementById('submit_comment');

    scrollToComment(userCommentInput);

    // The "comment" variable is given in encoded form is order to avoid error if user string contains symbols: ' ".
    userCommentInput.value = decodeURI(comment); 
    userCommentInput.setSelectionRange(comment.length, comment.length, 'forward');
    userCommentInput.focus();

    submitButton.innerHTML = 'Edit';
    editInput.value = 'edited';
    commentIDInput.value = commentID;

    if (!document.getElementById('cancel_edit')) {
        const cancelButton = createCancelButton();

        cancelButton.addEventListener('click', cancelCommentEditing.bind(
            cancelButton, submitButton, cancelButton, editInput,
            ));
        submitButton.after(cancelButton);
    }
}


function createCancelButton() {
    const newButton = document.createElement('button');
    newButton.classList.add('btn', 'btn-primary', 'f-s-12', 'rounded-corner', 'cancel_button');
    newButton.innerHTML = 'Cancel';
    newButton.id = 'cancel_edit';

    return newButton;
}


function cancelCommentEditing(submitButton, cancelButton, editInput, event) {
    // Cancel all changes which occurred during comment editing.
    event.preventDefault();
    changeCommentBlockClass();

    const commentInput = document.getElementById('usercomment-input');
    commentInput.value = '';

    submitButton.innerHTML = 'Comment';
    editInput.value = '';
    cancelButton.remove();
}


function changeTextarea(event) {
    event.target.style.height = 'auto';
    event.target.style.height = `${event.target.scrollHeight}px`;
}


function changeCommentBlockClass() {
    const commentBlock = document.getElementById('comment-block');

    if (commentBlock.classList.contains('comment-block')) {
        commentBlock.classList.remove('comment-block');
        commentBlock.classList.add('comment-block-edited');
    }
    else {
        commentBlock.classList.remove('comment-block-edited');
        commentBlock.classList.add('comment-block');
    }
}


function modifyEditedComments() {
    // If there are comments that have been edited, 
    // the function will modify 'edited' message depending on the length of a user's name.
    const editedComments = document.querySelectorAll('.edited_comment');
    if (editedComments.length > 0) {
        const userNameElements = document.querySelectorAll('.usercomment_name>a');

        for (let counter = 0; counter < editedComments.length; counter++) {
            setNewLeftValue(editedComments[counter], userNameElements[counter]);
        }
    }
}


function setNewLeftValue(editedElement, userNameElement) {
    const userNameWidth = getTextWidth(userNameElement.innerHTML, getComputedStyle(userNameElement).font);

    let leftValue = getComputedStyle(editedElement).getPropertyValue('left');
    leftValue = Number(leftValue.substring(0, leftValue.length - 2));
    editedElement.style.left = `${leftValue + userNameWidth}px`;
}


function getTextWidth(text, font) {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
  
    context.font = font || getComputedStyle(document.body).font;
  
    return context.measureText(text).width;
  }


document.addEventListener('DOMContentLoaded', main);