main_route = '/lectores'

$(document).ready(function () {
    $('#data_table').DataTable();
});

$(document).ajaxStart(function () { });

$(document).ajaxStop(function () {
    $.Toast.hideToast();
});


$('#new').click(function () {
    $('#ip').val('')
    $('#puerto').val('')
    $('#descripcion').val('')
    $('#email').val('')
    $('#tipo').val("A")
    $('#fksucursal').val('')


    verif_inputs('')
    $('#id_div').hide()
    $('#insert').show()
    $('#update').hide()
    validationInputSelects("form")
    $('#form').modal('show')
})


$('#insert').click(function () {
    notvalid = validationInputSelectsWithReturn("form");
    if (notvalid===false) {
        objeto = JSON.stringify({
            'ip': $('#ip').val(),
            'puerto': $('#puerto').val(),
            'descripcion': $('#descripcion').val(),
            'email': $('#email').val(),
            'tipo': $('#tipo').val(),
            'fksucursal': $('#fksucursal').val()
        })
        ajax_call('lectores_insert', {
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
            notvalid,
            'error'
        )
    }
})

$('#crear').click(function () {

        // ajax_call('lectores_extraer_marcaciones', {
        //         _xsrf: getCookie("_xsrf")
        //     }, null, function () {
        //         setTimeout(function () {
        //         window.location = main_route
        //     }, 2000);
        // })
        //
        obj = JSON.stringify({
            '_xsrf': getCookie("_xsrf")
        })

        ruta = "lectores_extraer_marcaciones";
        $.ajax({
            method: "POST",
            url: ruta,
            data: {_xsrf: getCookie("_xsrf"), object: obj},
            async: true,
                    beforeSend: function () {
               $("#rproc-loader").fadeIn(800);
               $("#new").hide();
            },
            success: function () {
               $("#rproc-loader").fadeOut(800);
               $("#new").show();
            }
        }).done(function (response) {
            response = JSON.parse(response)
            showMessage("Marcaciones Extraidas", 'success', 'ok');

        })

})


function attach_edit() {
    $('.edit').click(function () {
        obj = JSON.stringify({
            'id': parseInt(JSON.parse($(this).attr('data-json')))
        })
        ajax_call_get('lectores_update', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            $('#id').val(self.id),
            $('#ip').val(self.ip),
            $('#puerto').val(self.puerto),
            $('#descripcion').val(self.descripcion),
            $('#email').val(self.email),
            $('#tipo').val(self.tipo),
            $('#tipo').selectpicker('refresh'),
            $('#fksucursal').val(self.fksucursal),
            $('#fksucursal').selectpicker('refresh')

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
    notvalid = validationInputSelectsWithReturn("form");
    if (notvalid===false) {
        objeto = JSON.stringify({
            'id': parseInt($('#id').val()),
            'ip': $('#ip').val(),
            'puerto': $('#puerto').val(),
            'descripcion': $('#descripcion').val(),
            'email': $('#email').val(),
            'tipo': $('#tipo').val(),
            'fksucursal': $('#fksucursal').val()
        })
        ajax_call('lectores_update', {
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
            notvalid,
            'error'
        )
    }
})

$('#extraer').click(function () {
    obj = JSON.stringify({
            'id': parseInt(JSON.parse($(this).attr('data-json')))
        })
    ruta = 'lectores_obtener_marcaciones';

    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: true,
        beforeSend: function () {
           $("#rproc-loader").fadeIn(800);

        },
        success: function () {
           $("#rproc-loader").fadeOut(800);

        }
    }).done(function (response) {
        response=JSON.parse(response)
        showMessage("Marcaciones obtenidas correctamente", "success", "ok")


    })
});

reload_form()


$('.delete').click(function () {
    id = parseInt(JSON.parse($(this).attr('data-json')))
    enabled = false
    swal({
        title: "¿Desea dar de baja el lector?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#1565c0",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    }).then(function () {
        ajax_call('lectores_delete', {
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

validationKeyup("form");
validationSelectChange("form");