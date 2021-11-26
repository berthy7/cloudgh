main_route = '/tipoausencia'

$(document).ready(function () {
    $('#data_table').DataTable();
});

$(document).ajaxStart(function () {
});

$(document).ajaxStop(function () {
    $.Toast.hideToast();
});


$('#selec_duracion').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
})

$('#selec_duracion').change(function () {
    if ($('#selec_duracion').val() == "Medio dia"){
        $('#duracion').val(0)
        $('#duracion').show()
    }else if($('#selec_duracion').val() == "Ilimitado"){
        $('#duracion').val("")
        $('#duracion').hide()

    }else{
        $('#duracion').val(1)
        $('#duracion').show()
    }

});

$('#selec_disponibilidad').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
})

$('#selec_disponibilidad').change(function () {
    if ($('#selec_disponibilidad').val() == "Veces al mes"){
        $('#disponibilidad').val(1)
        $('#disponibilidad').show()
    }else{

        $('#disponibilidad').val('')
        $('#disponibilidad').hide()
    }

});

$('#tipo').change(function () {
    if ($('#tipo').val() == "Permiso"){
        $('#row_disponibilidad').show()
        $('#selec_duracion').val('Hora')
        $('#selec_duracion').selectpicker('refresh')

        $('#disponibilidad').val(1)
        $('#selec_disponibilidad').val('Veces al mes')
        $('#selec_disponibilidad').selectpicker('refresh')

    }else{
        
        $('#row_disponibilidad').hide()
        $('#selec_duracion').val('Dia')
        $('#selec_duracion').selectpicker('refresh')

        $('#disponibilidad').val('')
        $('#selec_disponibilidad').val('')
        $('#selec_disponibilidad').selectpicker('refresh')

    }

});


$('#new').click(function () {
    $('#nombre').val('')
    $('#descripcion').val('')
    $('#duracion').val(1)
    $('#disponibilidad').val(1)
    $('#selec_duracion').val('Hora')
    $('#selec_duracion').selectpicker('refresh')

    $('#selec_disponibilidad').val('Veces al mes')
    $('#selec_disponibilidad').selectpicker('refresh')

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
            'descripcion': $('#descripcion').val(),
            'tipo': $('#tipo').val(),
            'disponibilidad': $('#disponibilidad').val(),
            'selec_disponibilidad': $('#selec_disponibilidad').val(),
            'duracion': $('#duracion').val(),
            'selec_duracion': $('#selec_duracion').val()
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

            $('#disponibilidad').val(self.disponibilidad)
            $('#selec_disponibilidad').val(self.selec_disponibilidad)
            $('#selec_disponibilidad').selectpicker('refresh')

            $('#duracion').val(self.duracion)
            $('#selec_duracion').val(self.selec_duracion)
            $('#selec_duracion').selectpicker('refresh')


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
            'descripcion': $('#descripcion').val(),
            'tipo': $('#tipo').val(),
            'disponibilidad': $('#disponibilidad').val(),
            'selec_disponibilidad': $('#selec_disponibilidad').val(),
            'duracion': $('#duracion').val(),
            'selec_duracion': $('#selec_duracion').val()
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