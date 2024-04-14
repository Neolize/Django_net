"use strict";


function main() {
    scrollToPosts();
    addURLParametersToPagination();
}


function addChildReview(name, parent_id) {
    let userCommentInput = document.getElementById('usercomment-input');
    userCommentInput.innerHTML = `${name}, `;
    userCommentInput.setSelectionRange(userCommentInput.value.length, userCommentInput.value.length, 'forward');

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


function deletePost(event) {
    const answer = confirm('Are you sure you want to delete this post?');
    if (answer === false) {
        event.preventDefault();
    }
}

/**
 *  Function adds 'posts' parameter to a URL query string for all pagination pages
 *  if  this page has 'posts' parameter set in a URL querystring.
 */
function addURLParametersToPagination() {
    const urlParams = new URLSearchParams(window.location.search);
    const postsToShow = urlParams.get('posts');

    if(postsToShow) {
        const allLinkElements = document.querySelectorAll('[data-posts]')
        for (let link of allLinkElements) {
            link.href = `${link.href}&posts=${postsToShow}`;
        }   
    }
}


document.addEventListener('DOMContentLoaded', main);