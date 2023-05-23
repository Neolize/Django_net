"use strict";

// inputMask

let phoneInput = document.getElementById('form-edit__phone');
let inputMask = new Inputmask('+7 (999) 999-99-99');
inputMask.mask(phoneInput);