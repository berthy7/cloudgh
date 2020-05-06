main_route = '/tipoausencia'

$(document).ready(function () {
    $('#data_table').DataTable();
});

$(document).ajaxStart(function () {
});

$(document).ajaxStop(function () {
    $.Toast.hideToast();
});


$('#new').click(function () {
    $('#nombre').val('')
    $('#descripcion').val('')

    verif_inputs('')
    validationInputSelects("form")
    $('#id_div').hide()
    $('#insert').show()
    $('#update').hide()
    validationInputSelects("form")
    $('#form').modal('show')
})


$('#insert').click(function () {
    notvalid = validationInputSelectsWithReturn("form");
    if (notvalid === false) {
        objeto = JSON.stringify({
            'nombre': $('#nombre').val(),
            'descripcion': $('#descripcion').val()
        })
        ajax_call('tipoausencia_insert', {
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


function attach_edit() {
    $('.edit').click(function () {
        obj = JSON.stringify({
            'id': parseInt(JSON.parse($(this).attr('data-json')))
        })
        ajax_call_get('tipoausencia_update', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            $('#id').val(self.id)
            $('#nombre').val(self.nombre)
            $('#descripcion').val(self.descripcion)

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
    if (notvalid === false) {
        objeto = JSON.stringify({
            'id': parseInt($('#id').val()),
            'nombre': $('#nombre').val(),
            'descripcion': $('#descripcion').val()
        })
        ajax_call('tipoausencia_update', {
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
reload_form()

// function attach_delete(idcb) {
//         id = idcb
//         enabled = false
//         swal({
//             title: "Â¿Desea dar de baja el tipo de ausencia?",
//             type: "warning",
//             showCancelButton: true,
//             confirmButtonColor: "#1565c0",
//             cancelButtonColor: "#F44336",
//             confirmButtonText: "Aceptar",
//             cancelButtonText: "Cancelar"
//         }).then(function () {
//             ajax_call('tipoausencia_delete', {
//                 id: id,
//                 enabled: enabled,
//                 _xsrf: getCookie("_xsrf")
//             }, null, function () {
//                 setTimeout(function () {
//                     window.location = main_route
//                 }, 2000);
//             })
//         })
// }


$('.delete').click(function (e) {
    e.preventDefault()
    cb_delete = this
    b = $(this).prop('checked')
    if (!b) {
        cb_title = "¿Está seguro de que desea dar de baja el tipo de ausencia?"

    } else {
        cb_title = "¿Está seguro de que desea dar de alta el tipo de ausencia?"
    }
    swal({
        title: cb_title,
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#1565c0",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    }).then(function () {
        $(cb_delete).prop('checked', !$(cb_delete).is(':checked'))
        objeto = JSON.stringify({
            id: parseInt($(cb_delete).attr('data-id')),
            enabled: $(cb_delete).is(':checked')
        })
        ajax_call('tipoausencia_delete', {
            object: objeto,
            _xsrf: getCookie("_xsrf")
        }, null, function () {
            setTimeout(function () {
                window.location = main_route
            }, 2000);
        })
        $('#form').modal('hide')
    })
})


$(document).ready(function () {
    //Checkbox para delete
    // $(":checkbox.checkboxdelete").click(function(){
    //     //Obtener el id del checkbox actual
    //     let idcb = $(this).attr("id");
    //     attach_delete(idcb);
    //
    // })

});
validationKeyup("form");
validationSelectChange("form");