main_route = '/usuario_profile'

$('#modal_modificar_password').on('shown.bs.modal', function () {
    $('#actual_pass').focus();
})

function Open_Modal_Pass() {
    $('#actual_pass').val('')
    $('#new_pass').val('')
    $('#new_rpass').val('')

    $('#actual_pass').parent().addClass('focused')
    $('#new_pass').parent().addClass('focused')
    $('#new_rpass').parent().addClass('focused')
    $('#actual_pass').focus()
    $('#modal_modificar_password').modal('show');
}


function Modificar_Password() {
    id = $('#user_id').val()
    actual = $('#actual_pass').val()
    newp = $('#new_pass').val()
    newp1 = $('#new_rpass').val()
    objeto =JSON.stringify({'id' : id,'old_password' : actual,'new_password' : newp, 'new_password_2':newp1})

    if(newp==newp1) {
        $.ajax({
            url: "/usuario_update_password",
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
}


function Modificar_Perfil() {
    id = $('#user_id').val()
    username = $('#username_profile').val()
    objeto =JSON.stringify({'id' : id,'username' : username})

    $.ajax({
        url: "/usuario_update_profile",
        type: "post",
        data: {object:objeto, _xsrf: getCookie("_xsrf")},
    }).done(function (response) {
        valor = JSON.parse(response)

        if(valor.success) {
            swal(
                'Perfil modificado.',
                'Se modificó el perfil de usuario correctamente.',
                'success'
            )
        } else {
            swal(
                'Perfil no modificado.',
                'No se modificó el perfil de usuario.',
                'error'
            )
        }
    })
}


function Modificar_Autenticacion(elemento){
    cb_delete = elemento
    b = $(elemento).prop('checked')
    if (!b) {
        cb_title = "¿Deshabilitar Verficacion en  2 Pasos?"

    } else {
        cb_title = "¿Habilitar Verficacion en  2 Pasos?"
    }
    swal({
        title: cb_title,
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#673AB7",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    }).then(function () {
        $(cb_delete).prop('checked', !$(cb_delete).is(':checked'))
        objeto = JSON.stringify({
            id: parseInt($(cb_delete).attr('data-id')),
            estado: $(cb_delete).is(':checked')
        })
        ajax_call('usuario_actualizar_autenticacion', {
            object: objeto,
            _xsrf: getCookie("_xsrf")
        }, null, function () {

        })
    
    })
}

$('#see-pass').mousedown(function(){
    $("#ic-pass").css("color", "lightgrey");
    $("#actual_pass").prop("type", "text");
    $("#ic-pass").html("visibility");
});

$("#see-pass").mouseup(function(){
    $("#ic-pass").css("color", "grey");
    $("#actual_pass").prop("type", "password");
    $("#ic-pass").html("visibility_off");
});

$('#see-pass-nc').mousedown(function(){
    $("#ic-pass-nc").css("color", "lightgrey");
    $("#new_pass").prop("type", "text");
    $("#ic-pass-nc").html("visibility");
});

$("#see-pass-nc").mouseup(function(){
    $("#ic-pass-nc").css("color", "grey");
    $("#new_pass").prop("type", "password");
    $("#ic-pass-nc").html("visibility_off");
});

$('#see-pass-ncr').mousedown(function(){
    $("#ic-pass-ncr").css("color", "lightgrey");
    $("#new_rpass").prop("type", "text");
    $("#ic-pass-ncr").html("visibility");
});

$("#see-pass-ncr").mouseup(function(){
    $("#ic-pass-ncr").css("color", "grey");
    $("#new_rpass").prop("type", "password");
    $("#ic-pass-ncr").html("visibility_off");
});