function validationInputSelects(id) {
    var flag = false
    var elementsInput = document.querySelectorAll('#' + id + ' input[type=text]:enabled')
    var elementsSelect = document.querySelectorAll('#' + id + ' select')
    var elementsNumber = document.querySelectorAll('#' + id + ' input[type=number]:enabled')
    var elementsTextarea = document.querySelectorAll('#' + id + ' textarea:enabled')
    for (var i = 0; i < elementsInput.length; i++) {
        if (elementsInput[i].id != '')
            if (!elementsInput[i].checkValidity()) {
                printError(elementsInput[i], elementsInput[i].validationMessage)
                flag = true
            } else {
                eraseError(elementsInput[i])
            }
    }
    for (var i = 0; i < elementsNumber.length; i++) {
        if (elementsNumber[i].id != '')
            if (!elementsNumber[i].checkValidity()) {

                printError(elementsNumber[i], elementsNumber[i].validationMessage)
                flag = true
            } else {
                eraseError(elementsNumber[i])
            }
    }
    for (var i = 0; i < elementsSelect.length; i++) {

        if (!elementsSelect[i].checkValidity()) {

            printError(elementsSelect[i], elementsSelect[i].validationMessage)
            flag = true
        } else {
            eraseError(elementsSelect[i])
        }

    }
    for (var i = 0; i < elementsTextarea.length; i++) {
        if (elementsTextarea[i].id != '')
            if (!elementsTextarea[i].checkValidity()) {
                //console.log(elementsInput[i])
                printError(elementsTextarea[i], elementsTextarea[i].validationMessage)
                flag = true
            } else {
                eraseError(elementsTextarea[i])
            }
    }

    return flag
}

function validationInputSelectsWithReturn(id) {
    var flag = false;
    var elementsInput = document.querySelectorAll('#' + id + ' input[type=text]:enabled')
    var elementsSelect = document.querySelectorAll('#' + id + ' select')
    var elementsNumber = document.querySelectorAll('#' + id + ' input[type=number]:enabled')
    var elementsTextarea = document.querySelectorAll('#' + id + ' textarea:enabled')

    for (var i = 0; i < elementsInput.length; i++) {
        if (elementsInput[i].id != '')
            if (!elementsInput[i].checkValidity()) {
                //console.log(elementsInput[i])
                printError(elementsInput[i], elementsInput[i].validationMessage)
                flag = true
                message = "Por favor completa el campo " + elementsInput[i].name;
                return message;
            } else {
                eraseError(elementsInput[i])
            }
    }
    for (var i = 0; i < elementsNumber.length; i++) {
        if (elementsNumber[i].id != '')
            if (!elementsNumber[i].checkValidity()) {
                //console.log(elementsNumber[i])
                printError(elementsNumber[i], elementsNumber[i].validationMessage)
                flag = true
            } else {
                eraseError(elementsNumber[i])
            }
    }
    for (var i = 0; i < elementsTextarea.length; i++) {
        if (elementsTextarea[i].id != '')
            if (!elementsTextarea[i].checkValidity()) {
                //console.log(elementsInput[i])
                printError(elementsTextarea[i], elementsTextarea[i].validationMessage)
                flag = true
                message = "Por favor completa el campo " + elementsTextarea[i].name;
                return message;
            } else {
                eraseError(elementsTextarea[i])
            }
    }

    for (var i = 0; i < elementsSelect.length; i++) {
        if (!elementsSelect[i].checkValidity()) {
            console.log(elementsSelect[i])
            printError(elementsSelect[i], elementsSelect[i].validationMessage);
            flag = true;
            return elementsSelect[i].querySelector('.bs-title-option').text;
        } else {
            eraseError(elementsSelect[i])
        }

    }

    return flag
}

function disabledInputSelects(id) {
    var flag = false
    var elementsInput = document.querySelectorAll('#' + id + ' input[type=text]')
    var elementsSelect = document.querySelectorAll('#' + id + ' select')
    var elementsButton = document.querySelectorAll('#' + id + ' button')
    var elementsCheck = document.querySelectorAll('#' + id + ' input[type=checkbox]')
    var elementsFile = document.querySelectorAll('#' + id + ' input[type=file]')
    for (var i = 0; i < elementsInput.length; i++) {

        elementsInput[i].disabled = true

    }
    for (var i = 0; i < elementsSelect.length; i++) {

        elementsSelect[i].disabled = true
    }
    for (var i = 0; i < elementsButton.length; i++) {


        elementsButton[i].disabled = true
    }
    for (var i = 0; i < elementsCheck.length; i++) {

        elementsCheck[i].disabled = true
    }
    for (var i = 0; i < elementsFile.length; i++) {
        elementsFile[i].disabled = true

    }

    return flag
}

function enabledInputSelects(id) {
    var flag = false
    var elementsInput = document.querySelectorAll('#' + id + ' input[type=text]')
    var elementsSelect = document.querySelectorAll('#' + id + ' select')
    var elementsButton = document.querySelectorAll('#' + id + ' button')
    var elementsCheck = document.querySelectorAll('#' + id + ' input[type=checkbox]')
    var elementsFile = document.querySelectorAll('#' + id + ' input[type=file]')
    for (var i = 0; i < elementsInput.length; i++) {

        elementsInput[i].disabled = false

    }
    for (var i = 0; i < elementsSelect.length; i++) {

        elementsSelect[i].disabled = false
    }
    for (var i = 0; i < elementsButton.length; i++) {

        elementsButton[i].disabled = false
    }
    for (var i = 0; i < elementsCheck.length; i++) {

        elementsCheck[i].disabled = false
    }
    for (var i = 0; i < elementsFile.length; i++) {
        elementsFile[i].disabled = false

    }

    return flag
}

function printError(element, validMessage) {
    element.parentElement.classList.add("error")
    if (!document.getElementById('errorMsg_' + element.id)) {
        labelError = document.createElement("label");
        // labelError.appendChild(labelErrorText);
        labelError.setAttribute('id', "errorMsg_" + element.id)
        labelError.classList.add("error");
        labelError.classList.add("text-danger");
        labelError.innerHTML = validMessage;
        element.parentElement.insertAdjacentElement("afterend", labelError);
    }
}

function validationKeyup(id) {
    var elementsInput = document.querySelectorAll('#' + id + ' input[type=text]')
    var elementsNumber = document.querySelectorAll('#' + id + ' input[type=number]:enabled')
    for (var i = 0; i < elementsInput.length; i++) {

        if (elementsInput[i].id != '')
            elementsInput[i].oninput = function () {
                if (!this.checkValidity()) {
                    printError(this, this.validationMessage)
                } else {
                    eraseError(this)
                }
            }
    }
    for (var i = 0; i < elementsNumber.length; i++) {

        if (elementsNumber[i].id != '')
            elementsNumber[i].oninput = function () {
                if (!this.checkValidity()) {
                    printError(this, this.validationMessage)
                } else {
                    eraseError(this)
                }
            }
    }
}

function validationSelectChange(id) {
    var elementsSelect = document.querySelectorAll('#' + id + ' select')
    for (var i = 0; i < elementsSelect.length; i++) {

        elementsSelect[i].addEventListener('change', function () {
            if (this.value != 0)
                eraseError(this)
        })
        if (!elementsSelect[i].checkValidity()) {

            printError(elementsSelect[i], elementsSelect[i].validationMessage)
        }
    }
}

function eraseError(element) {
    if (document.getElementById('errorMsg_' + element.id)) {
        eleChild = document.getElementById('errorMsg_' + element.id)
        element.parentElement.classList.remove('error');
        eleChild.parentElement.removeChild(eleChild)
    }

}

function esNumero(ele) {
    let vector = [];
    vector.push(!isNaN(ele));
    return vector;
}

function validarLongitudHora(id) {
    var flag = false;
    var elementsInput = document.querySelectorAll('#' + id + ' input[type=text]:enabled')

    for (var i = 0; i < elementsInput.length; i++) {
        if (elementsInput[i].id != '')
            var stringHora = elementsInput[i].value;
        stringHora = stringHora.split(':');
        var bandera = (stringHora.map(a => esNumero(a))).flat();
        let arrayTrue = arr => arr.every(v => v === true);
        bandera = arrayTrue(bandera);
        if (!bandera) {
            return bandera;
        }
    }
    return true;
}

// function validarHorarios(id) {
//     var flag = false;
//     var elementsInput = document.querySelectorAll('#' + id + ' input[type=text]:enabled')
//
//     for (var i = 0; i < elementsInput.length; i++) {
//         if (elementsInput[i].id != '')
//             var stringHora = elementsInput[i].value;
//         moment();
//         stringHora = stringHora.split(':');
//         var bandera = (stringHora.map(a => esNumero(a))).flat();
//         let arrayTrue = arr => arr.every(v => v === true);
//         bandera = arrayTrue(bandera);
//         if (!bandera) {
//             return bandera;
//         }
//     }
//     return true;
// }

function validarConflictoHorarios(id) {
    /*
      0 2 4   1 3 5   Primer horario
      6 8 10  7 9 11  Segundo horario
      */
    var flag = false;
    let elementsInput = document.querySelectorAll('#' + id + ' input[type=text]:enabled');
    let longitud = elementsInput.length;
    let elementsInputOrdenado = [];
    let arrayHorarios = [];
    let arrayMoment = [];
    let arrayDiferencias = [];

    for (let i = 0; i < longitud; i+=6) {
        elementsInputOrdenado.push([elementsInput[i], elementsInput[i+2], elementsInput[i+4]]);
        elementsInputOrdenado.push([elementsInput[i+1], elementsInput[i+3], elementsInput[i+5]]);
    }
    // Elementos Input de manera ordenada, contiene una matriz de 2x3, cada fila representa entrada y salida
    // console.log("elementsInputOrdenado");
    // console.log(elementsInputOrdenado);

    for (let i = 0; i < elementsInputOrdenado.length; i++) {
        arrayMoment.push(castMoment(elementsInputOrdenado[i]));
    }

    // Array Moment, matriz de 2x3, tiene objetos tipo Moment
    // console.log("arrayMoment");
    // console.log(arrayMoment);

    for (let i = 0; i < arrayMoment.length; i++) {
        arrayDiferencias.push(diferenciaHorarios(arrayMoment[i]));
    }

    // ArrayDiferencias, matriz de 2x1, representa la diferencia entre los horarios de cada fila
    // console.log("arrayDiferencias");
    // console.log(arrayDiferencias);

    for (let j = 0; j < arrayDiferencias.length ; j++) {
        let x = arrayDiferencias[j];
        let allTrue = x.every(elemento => elemento > 0);
        if(!allTrue){
            flag = printErrorArray(x, j, elementsInputOrdenado);
        }
    }

    return flag;
}

function castMoment(arrayString) {
    let arrayTemporal = [];
    for (let i = 0; i < arrayString.length; i++) {
        // let a = moment(arrayString[i].value, "HH mm");
        // arrayTemporal.push(a);
        arrayTemporal.push(moment(arrayString[i].value, "HH mm"));
    }
    return arrayTemporal;
}

function diferenciaHorarios(arrayString) {
    let arrayTemporal = [];
    for (let i = 0; i < arrayString.length-1; i++) {
        // let a = arrayString[i];
        // let b = arrayString[i+1];
        // let c = b.diff(a, 'minutes');
        // arrayTemporal.push(c);
        arrayTemporal.push(arrayString[i+1].diff(arrayString[i], 'minutes'));
    }
    return arrayTemporal;
}

function printErrorArray(arrayString, index, elementsInputOrdenado) {
    for (let i = 0; i < arrayString.length; i++) {
        let a = arrayString[i];
        if(a<=0){
            printError(elementsInputOrdenado[index][i], "conflicto de horario");
            printError(elementsInputOrdenado[index][i+1], "conflicto de horario");
            message = "Conflicto de horario entre: " + elementsInputOrdenado[index][i].name +" y "+ elementsInputOrdenado[index][i+1].name;
            return message;
        }else{
            eraseError(elementsInputOrdenado[index][i]);
            eraseError(elementsInputOrdenado[index][i+1]);
        }
    }
    return true;
}