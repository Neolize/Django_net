"use strict";


function deleteGroup(event) {
    const answer = confirm('Are you sure you want to delete this group?');
    if (answer === false) {
        event.preventDefault();
    }
}