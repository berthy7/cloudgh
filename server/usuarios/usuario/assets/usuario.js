main_route = '/usuario'

$(document).ready(function () {
    $('#data_table').DataTable();
    $('.error').addClass("error-own");
});

$('.dd').nestable({
    group:'categories',
    maxDepth:0,
    reject: [{
        rule: function () {
            // The this object refers to dragRootEl i.e. the dragged element.
            // The drag action is cancelled if this function returns true
            var ils = $(this).find('>ol.dd-list > li.dd-item');
            for (var i = 0; i < ils.length; i++) {
                var datatype = $(ils[i]).data('type');
                if (datatype === 'child')
                    return true;
            }
            return false;
        },
        action: function (nestable) {
            // This optional function defines what to do when such a rule applies. The this object still refers to the dragged element,
            // and nestable is, well, the nestable root element
            alert('Can not move this item to the root');
        }
    }]
});

$('.module').click(function () {
    var checked = $(this).prop('checked')
    //$('.module').prop('checked', false)
    empresa_id = null
    sucursal_id = null
    gerencia_id = null
    grupo_id = null
    emp_id = null
    if ($(this).hasClass('employee')){
        emp_id = parseInt($(this).attr('data-id'))
    } else {
        if ($(this).hasClass('grupo')){
            grupo_id = parseInt($(this).attr('data-id'))
            gerencia_id = parseInt($(this).attr('data-ger'))
            sucursal_id = parseInt($(this).attr('data-suc'))
            empresa_id = parseInt($(this).attr('data-empr'))
        } else {
            if ($(this).hasClass('gerencia')){
                gerencia_id = parseInt($(this).attr('data-id'))
                sucursal_id = parseInt($(this).attr('data-suc'))
                empresa_id = parseInt($(this).attr('data-empr'))
            }else {
                if($(this).hasClass('sucursal')){
                    sucursal_id = parseInt($(this).attr('data-id'))
                    empresa_id = parseInt($(this).attr('data-empr'))
                }else {
                    if($(this).hasClass('empresa')){
                        empresa_id_id = parseInt($(this).attr('data-id'))
                    }
                }
            }
        }
    }
    $(this).prop('checked', checked)
    $(this).parent().next().find('.module').prop('checked', $(this).prop('checked'))
    analizar($(this).parent().parent().closest('.dd-list').prev().find('.module'))
})

function analizar(parent) {
    children = $(parent).parent().next().find('.module:checked')
    //console.log(children.length)
    $(parent).prop('checked', (children.length > 0))
    grand_parent = $(parent).parent().parent().closest('.dd-list').prev().find('.module')
    //console.log(grand_parent.length)
    if (grand_parent.length > 0){
        analizar(grand_parent)
    }
}

function obtener_personas_arbol() {
    aux = []
    $('.employee:checked').each(function () {
        var a = parseInt($(this).attr('data-id'))

        aux.push((function add(a) {

            return {
                'id_persona': a
            }


        })(a))
    })
    return aux
}

$('#role_id').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar rol.',
    title: 'Seleccione un rol.'
})

$('#fkpersona').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar persona',
    title: 'Seleccione una persona'
})
attach_validators()


$('#new').click(function () {
    $('#id').val('')
    $('#username').val('')
    $('#password').val('')

    $('#role_id').val('')
    $('#role_id').selectpicker('refresh')

    $('#fkpersona').val('')
    $('#fkpersona').selectpicker('refresh')

    verif_inputs('')
    validationInputSelects("form")
    $('#id_div').hide()
    $('#insert').show()
    $('#pass').show()
    $('#update').hide()

    $('#form').modal('show')
})


$('#insert').click(function () {
    notvalid = validationInputSelectsWithReturn("form");
    if (notvalid===false) {

        objeto = JSON.stringify({
        'username': $('#username').val(),
        'password': $('#password').val(),
        'fkrol': parseInt($('#role_id').val()),
        'fkpersona': parseInt($('#fkpersona').val())
        })

        ajax_call('usuario_insert', {
            _xsrf: getCookie("_xsrf"),
            object: objeto
        }, null, function (response) {
            response = JSON.parse(response);
            if(response.success === true){
                setTimeout(function(){window.location=main_route}, 2000);
            }else{

                swal(
                    'Datos duplicados',
                    response.message,
                    'error'
                )
            }

        })
        $('#form').modal('hide')
    }else{
        swal(
            'Error de datos.',
            notvalid,
            'error'
        )
    }
})

$('#new_usuarios').click(function () {

    $('#rol_usuarios').val('')
    $('#rol_usuarios').selectpicker('refresh')
    $('.module').prop('checked', false)

    verif_inputs('')
    validationInputSelects("form_usuarios")


    $('#insert_usuarios').show()
    $('#form_usuarios').modal('show')
})

$('#insert_usuarios').click(function () {
    notvalid = validationInputSelectsWithReturn("form_usuarios");
    if (notvalid===false) {
        objeto = JSON.stringify({
            'fkrol': parseInt($('#rol_usuarios').val()),
            'personas_arbol': obtener_personas_arbol()
            })

        ajax_call('usuario_registrar', {
            object: objeto,
            _xsrf: getCookie("_xsrf")
        }, null, function () {
            setTimeout(function () {
                window.location = main_route
            }, 2000);
        })
        $('#form_usuarios').modal('hide')
     } else {
        swal(
            'Error de datos.',
             notvalid,
            'error'
        )
    }
})




function attach_edit() {
    $('.edit').click(function () {
        obj = JSON.stringify({
            'id': parseInt(JSON.parse($(this).attr('data-json')))
        })
        ajax_call_get('usuario_update',{
            _xsrf: getCookie("_xsrf"),
            object: obj
        },function(response){
            var self = response;

            $('#id').val(self.id)
            $('#username').val(self.username)
            $('#password').val(self.password)
            $('#role_id').val(self.fkrol)
            $('#role_id').selectpicker('render')

            $('#fkpersona').val(self.fkpersona)
            $('#fkpersona').selectpicker('render')

            clean_form()
            verif_inputs('')
            $('#id_div').hide()
            $('#insert').hide()
            $('#update').show()
            $('#pass').hide()
            $('#form').modal('show')
        })
    })
}
attach_edit()


$('#update').click(function () {
    objeto = JSON.stringify({
        'id': parseInt($('#id').val()),
        'username': $('#username').val(),
        'password': $('#password').val(),
        'fkrol': parseInt($('#role_id').val()),
        'fkpersona': parseInt($('#fkpersona').val())
    })
        ajax_call('usuario_update', {
            _xsrf: getCookie("_xsrf"),
            object: objeto
        }, null, function (response) {
            response = JSON.parse(response);
            if(response.success === true){
                setTimeout(function(){window.location=main_route}, 2000);
            }else{

                swal(
                    'Datos duplicados',
                    response.message,
                    'error'
                )
            }

        })
    $('#form').modal('hide')
})
reload_form()
$('#role_id').selectpicker()


var verificar = false
idu = 0
$('.delete').click(function(e) {
    e.preventDefault()
    cb_delete = this
    b = $(this).prop('checked')
    idu = $(this).prop('id')

    if(!b){
        cb_title = "¿Está seguro de que desea dar de baja al Usuario?"
    } else {
        cb_title ="¿Está seguro de que desea dar de alta al Usuario?"
    }
    swal({
        text: cb_title,
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#004c99",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    }).then(function () {
        verificar = !$(cb_delete).is(':checked')
        $(cb_delete).prop('checked', !$(cb_delete).is(':checked'))

        if(b) $(cb_delete).parent().prop('title', 'Activo')
        else $(cb_delete).parent().prop('title', 'Inhabilitado')

        objeto =JSON.stringify({
            id: parseInt($(cb_delete).attr('data-id')),
            enabled: $(cb_delete).is(':checked')
        })

        ajax_call('usuario_delete', {
            object:
                objeto,_xsrf: getCookie("_xsrf")
            }, null, function (resp) {
                var self = JSON.parse(resp)
                if(self.success){
                    $('#'+idu).prop('checked', verificar)
                }else{
                    $('#'+idu).prop('checked', false)
                    $('#'+idu).parent().prop('title', 'Inhabilitado')
                }
            }
        )
        $('#form').modal('hide')
    })
})


$('#modificar_password').on('shown.bs.modal', function () {
    $('#new_pass').focus();
})


$('.reset').click(function () {
    id = parseInt(JSON.parse($(this).attr('data-json')))

    $('#new_pass').val('')
    $('#new_rpass').val('')
    $('#new_pass').parent().addClass('focused')
    $('#new_rpass').parent().addClass('focused')
    $('#actual_pass').focus()
    $('#id_usuario').val(id)
    $('#modificar_password').modal('show');
})


function Modificar_Contraseña() {
    values="new_pass,new_rpass";

    if(validate_inputs_empty(values)) {
        swal({
            title: "Desea modificar la contraseña al usuario?",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#4CAF50",
            cancelButtonColor: "#F44336",
            confirmButtonText: "Aceptar",
            cancelButtonText: "Cancelar"
        }).then(function () {
            id = $('#id_usuario').val()
            newp = $('#new_pass').val()
            newp1 = $('#new_rpass').val()
            objeto =JSON.stringify({'id' : id,'new_password' : newp, 'new_password_2':newp1})

            if(newp==newp1) {
                $.ajax({
                    url: "/usuario_reset_password",
                    type: "post",
                    data: {object:objeto, _xsrf: getCookie("_xsrf")},
                }).done(function (response) {
                    valor=JSON.parse(response)
                    if(valor.success) {
                        swal(
                            'Contraseña modificada.',
                            'Se modificó la contraseña correctamente.',
                            'success'
                        )
                    } else {
                        swal(
                            'Contraseña actual errónea.',
                            'No se modificó la contraseña.',
                            'error'
                        )
                    }
                })
            } else {
                swal(
                    'Error de datos.',
                    'Las contraseñas no coinciden.',
                    'error'
                )
            }
        })
    } else {
        swal(
            'Error de datos.',
            'Hay campos vacíos por favor verifique sus datos.',
            'error'
        )
    }
}


$('.reset1').click(function () {
    id = parseInt(JSON.parse($(this).attr('data-json')))

    swal({
        title: "Desea anular el dispositivo y habilitar nuevamente al usuario?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#1565c0",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    }).then(function () {
        ajax_call("/usuario_codigo_reset", { id: id,_xsrf: getCookie("_xsrf")}, null, function () {setTimeout(function(){window.location=main_route}, 2000);})
    })
})

validationKeyup("form")
validationSelectChange("form")

//Verificar el campo de password
function validationPassword(id) {
    var flag = false
    var elementsInput = document.querySelectorAll('#'+id+' input[type=password]:enabled')
    for (var i = 0; i < elementsInput.length; i++) {
        if (elementsInput[i].id != '') {
            if (!elementsInput[i].checkValidity()) {
                printError(elementsInput[i], elementsInput[i].validationMessage)
                flag = true
            } else {
                eraseError(elementsInput[i])
            }
        }
    }
    return flag
}




/////////////////////////////////////////////////////////
//     ajax_call_post("usuario_verificar_username", {
//         _xsrf: getCookie("_xsrf"),
//         object: objeto_verificar
//         }, function (response) {
//             if(response.success === true){
//                
//
//
//
//
//
//
//             }else{
//                 swal(
//                     'Usuario en uso',
//                     'El usuario ya se encuentra, en uso porfavor, ingrese otro correo electronico',
//                     'warning' )
//             }
//
//         });