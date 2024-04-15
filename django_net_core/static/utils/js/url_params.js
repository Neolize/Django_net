"use strict";


/**
 *  Function adds 'posts' parameter to a URL query string for all pagination pages, edit link, and delete link
 *  if  this page has 'posts' parameter set in a URL querystring.
 */
function addURLParameters() {
    const urlParams = new URLSearchParams(window.location.search);
    const postsToShow = urlParams.get('posts');
    const postForm = document.getElementById('post_form');

    if (postsToShow) {
        addURLParametersToPagination(postsToShow);
        addURLParametersToEditLink(postsToShow);
        addURLParametersToDeleteLink(postsToShow);
    }
    if (postForm) {
        addURLParametersToEditingPage(postsToShow);
    }
}


function addURLParametersToPagination(postsToShow) {
    const allLinkElements = document.querySelectorAll('[data-posts]');
    if (allLinkElements) {
        for (let link of allLinkElements) {
            link.href = `${link.href}&posts=${postsToShow}`;
        }
    }
}


function addURLParametersToEditLink(postsToShow) {
    const editLink = document.querySelector('[data-posts-edit]');
    if (editLink) {
        editLink.href = `${editLink.href}?posts=${postsToShow}`;
    }
}


function addURLParametersToDeleteLink(postsToShow) {
    const deleteLink = document.querySelector('[data-posts-delete]');
    if (deleteLink) {
        deleteLink.href = `${deleteLink.href}?posts=${postsToShow}`;
    }
}


function addURLParametersToEditingPage(postsToShow) {
    const editButton = document.querySelector('[data-edit-button]');
    if (editButton) {
        let inputElement = document.getElementById('edit-post-input');
        inputElement.value = postsToShow;
    }
}


document.addEventListener('DOMContentLoaded', addURLParameters);