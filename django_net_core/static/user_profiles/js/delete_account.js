"use strict";


function deleteAccount(event) {
    const answer = confirm('Are you sure you want to delete your account?');
    if (answer === false) {
        event.preventDefault();
    }
}