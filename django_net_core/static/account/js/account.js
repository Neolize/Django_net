"use strict";


function main() {
    let signupInstance = new AccountSignup();
    signupInstance.initiateSearch();
}


class AccountSignup {
    constructor() {
        this.increasedBlocksNumber = 0;
        this.form = document.getElementById('account-signup-form');
        this.marginBottom = 25;
    }

    searchNonFieldErrorsBlock(obj) {
        let blocks = obj.form.querySelectorAll('[data-identifier]');

        if (blocks && blocks.length > obj.increasedBlocksNumber ) {
            let height = 0
            if (blocks.length > 1) {
                for (let item of blocks) {
                    obj.increasedBlocksNumber++;
                    height = height + item.offsetHeight + obj.marginBottom;
                }
            }
            else {
                obj.increasedBlocksNumber++;
                height = blocks[0].offsetHeight + obj.marginBottom;
            }
            obj.increaseSignupForm(height);
        }
    }

    increaseSignupForm(increaseDegree) {
        this.form.style.height = `${this.form.offsetHeight + increaseDegree}px`;
    }

    initiateSearch() {
        setInterval(this.searchNonFieldErrorsBlock, 100, this);
    }
}


document.addEventListener('DOMContentLoaded', main);