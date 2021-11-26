main_route = '/ajustes'


$(document).ajaxStart(function () { });

$(document).ajaxStop(function () {
    $.Toast.hideToast();
});

$(".hr").inputmask("h:s",{ "placeholder": "__/__" });

$('#new').click(function () {
    $('#nombre').val('')

    verif_inputs('')
    $('#id_div').hide()
    $('#insert').show()
    $('#update').hide()
    $('#form').modal('show')
})


$('#insert').click(function () {
    values = "nombre";
    if (validate_inputs_empty(values)) {
        objeto = JSON.stringify({
            'nombre': $('#nombre').val()
        })
        ajax_call('ajustes_insert', {
            object: objeto,
            _xsrf: getCookie("_xsrf")
        }, null, function () {
            setTimeout(function () {
                window.location = main_route
            }, 2000);
        })
        $('#form').modal('hide')
    } else {
        swal(
            'Error de datos.',
            'Hay campos vacíos por favor verifique sus datos.',
            'error'
        )
    }
})


function attach_edit() {
    $('.edit').click(function () {
        obj = JSON.stringify({
            'id': parseInt(JSON.parse($(this).attr('data-json')))
        })
        ajax_call_get('ajustes_update', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            $('#id').val(self.id)
            $('#nombre').val(self.nombre)

            clean_form()
            verif_inputs('')
            $('#id_div').hide()
            $('#insert').hide()
            $('#update').show()
            $('#form').modal('show')
        })
    })
}
attach_edit()


$('#update').click(function () {
    if (!validationInputSelects("form")) {
        objeto = JSON.stringify({
            'id': parseInt($('#id').val()),
            'nombre': $('#nombre').val()
        })
        ajax_call('ajustes_update', {
            object: objeto,
            _xsrf: getCookie("_xsrf")
        }, null, function () {
            setTimeout(function () {
                window.location = main_route
            }, 2000);
        })
        $('#form').modal('hide')
    } else {
        swal(
            'Error de datos.',
            'Hay campos vacíos por favor verifique sus datos.',
            'error'
        )
    }
})
reload_form()


$('.delete').click(function () {
    id = parseInt(JSON.parse($(this).attr('data-json')))
    enabled = false
    swal({
        title: "¿Desea dar de baja los datos del país?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#1565c0",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    }).then(function () {
        ajax_call('ajustes_delete', {
            id: id,
            enabled: enabled,
            _xsrf: getCookie("_xsrf")
        }, null, function () {
            setTimeout(function () {
                window.location = main_route
            }, 2000);
        })
    })
})


$('#actualizar').click(function () {

    objeto = JSON.stringify({
        'dominio': $('#dominio').val(),
        'mysql': document.getElementById('checkMysql').checked,
        'postgres': document.getElementById('checkPostgres').checked,
        'oracle': document.getElementById('checkOracle').checked,
        'sqlserver': document.getElementById('checkSqlServer').checked
    })
    ajax_call('ajustes_update', {
        object: objeto,
        _xsrf: getCookie("_xsrf")
    }, null, function () {
        setTimeout(function () {
            window.location = main_route
        }, 2000);
    })

})