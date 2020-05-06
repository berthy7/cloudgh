main_route = '/portal_ausencia'

$(document).ready(function () {
    $('#data_table').DataTable();
    $('#data_table_recibidas').DataTable();


});

    document.getElementById("primero").click();

    $('#primero').click(function () {
        $('#body-cont').css("display", "block")
        $('#body-elfec').css("display", "none")
    })

    $('#segundo').click(function () {
        $('#body-cont').css("display", "none")
        $('#body-elfec').css("display", "block")
    })

$(document).ajaxStart(function () { });

$(document).ajaxStop(function () {
    $.Toast.hideToast();
});
$(".hr").inputmask("h:s",{ "placeholder": "__/__" });

$('.date').bootstrapMaterialDatePicker({
    format: 'DD/MM/YYYY',
    clearButton: false,
    weekStart: 1,
    locale: 'es',
    time: false
}).on('change', function (e, date) {
    $(this).parent().addClass('focused');
    eraseError(this)
});
$('.datepicker').bootstrapMaterialDatePicker({
    format: 'DD/MM/YYYY',
    clearButton: false,
    weekStart: 1,
    locale: 'es',
    time: false
}).on('change', function (e, date) {
    $(this).parent().addClass('focused');
    $('#f_date').bootstrapMaterialDatePicker('setMinDate', date);
});

$('#fktipoausencia').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar ausencia',
    title: 'Seleccione el tipo de ausencia'
})

$('#fkpersona').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar persona',
    title: 'Seleccione una persona'
})


$('#new').click(function () {
    $('#nombre').val($('#pnombre').val())
    $('#estado').val('Pendiente')
    $('#fktipoausencia').val('')
    $('#fktipoausencia').selectpicker('refresh')
    $('#fkpersona').val('')
    $('#fkpersona').selectpicker('refresh')
    $('#descripcion').val('')

    $('#fechai').val('')
    $('#horai').val('')
    $('#fechaf').val('')
    $('#horaf').val('')


    verif_inputs('')
    validationInputSelects("form")
    $('#id_div').hide()
    $('#insert').show()
    $('#update').hide()
    $('#update_superior').hide()
    $('#respuesta_superior').hide()
    validationInputSelects("form")
    $('#form').modal('show')
})


$('#insert').click(function () {
    notvalid = validationInputSelectsWithReturn("form");
    if (notvalid===false) {
        objeto = JSON.stringify({
            'fktipoausencia': $('#fktipoausencia').val(),
            'fkpersona': $('#pid').val(),
            'descripcion': $('#descripcion').val(),
            'fechai': $('#fechai').val(),
            'horai': $('#horai').val(),
            'fechaf': $('#fechaf').val(),
            'horaf': $('#horaf').val()

        })
        
        objeto_verificar = JSON.stringify({
            'fkpersona': $('#pid').val(),
            'fechai': $('#fechai').val(),
            'fechaf': $('#fechaf').val()

        })

        ajax_call_post("v_personal_disponible", {
            _xsrf: getCookie("_xsrf"),
            object: objeto_verificar
            }, function (response) {
                if(response.success === true){
                    ajax_call('portal_ausencia_insert', {
                        object: objeto,
                            _xsrf: getCookie("_xsrf")
                        }, null, function () {
                            setTimeout(function () {
                            window.location = main_route
                        }, 2000);
                    })
                    $('#form').modal('hide')



                }else{
                    swal(
                        'No se pudo procesar.',
                        response.message,
                        response.tipo )
                }

            });

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
        ajax_call_get('portal_ausencia_update', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            $('#id').val(self.id)
            $('#nombre').val($('#pnombre').val())
            $('#estado').val(self.estado)
            $('#fktipoausencia').val(self.fktipoausencia)
            $('#fktipoausencia').selectpicker('refresh')
            $('#pid').val(self.fkpersona)
            $('#descripcion').val(self.descripcion)
            $('#fechai').val(self.fechai)
            $('#horai').val(self.horai)
            $('#fechaf').val(self.fechaf)
            $('#horaf').val(self.horaf)

            if (self.estado =="Pendiente"){
                $('#update').show()
            }else{
                $('#update').hide()
            }

            if (self.respuesta !=""){
                console.log("entro")

                $('#respuesta_superior').show()
                $('.botones_autorizacion').hide()
                $('#respuesta').val(self.respuesta)
            }else{
                $('#respuesta_superior').hide()
            }


            // clean_form()
            validationInputSelects("form")
            $('#id_div').hide()
            $('#insert').hide()
            $('#update_superior').hide()

            $('#form').modal('show')
        })
    })

    $('.edit_recibidas').click(function () {
        obj = JSON.stringify({
            'id': parseInt(JSON.parse($(this).attr('data-json')))
        })
        ajax_call_get('portal_ausencia_update', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            $('#id').val(self.id)
            $('#nombre').val(self.persona.fullname)
            $('#estado').val(self.estado)
            $('#fktipoausencia').val(self.fktipoausencia)
            $('#fktipoausencia').selectpicker('refresh')
            $('#pid').val(self.fkpersona)
            $('#descripcion').val(self.descripcion)
            $('#fechai').val(self.fechai)
            $('#horai').val(self.horai)
            $('#fechaf').val(self.fechaf)
            $('#horaf').val(self.horaf)
            $('#autorizar').val(self.estado)
            $('#autorizar').selectpicker('refresh')
            $('#respuesta').val(self.respuesta)

            if (self.estado =="Aceptado"){
                $('#update').hide()
            }else{
                $('#update').show()
            }

            clean_form()
            verif_inputs('')
            $('#id_div').hide()
            $('#insert').hide()
            $('#update').hide()
            $('#respuesta_superior').show()
            $('#update_superior').show()
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
            'fktipoausencia': $('#fktipoausencia').val(),
            'fkpersona': $('#pid').val(),
            'descripcion': $('#descripcion').val(),
            'fechai': $('#fechai').val(),
            'horai': $('#horai').val(),
            'fechaf': $('#fechaf').val(),
            'horaf': $('#horaf').val()
        })
        ajax_call('portal_ausencia_update', {
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

$('#update_superior').click(function () {
    if (!validationInputSelects("form")) {
        objeto = JSON.stringify({
            'id': parseInt($('#id').val()),
            'estado': $('#estado').val(),
            'respuesta': $('#respuesta').val()
        })
        ajax_call('portal_ausencia_update_superior', {
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
        title: "¿Desea dar de baja los datos de la ausencia?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#1565c0",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    }).then(function () {
        ajax_call('portal_ausencia_delete', {
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


$('#aceptado').click(function () {
    $('#estado').val('Aceptado')
    $('#estado').parent().addClass('focused')
    $("#estado").attr("disabled", true).css("background-color","#25AE88");

})

$('#pendiente').click(function () {
    $('#estado').val('Pendiente')
    $('#estado').parent().addClass('focused')
    $("#estado").attr("disabled", true).css("background-color","#ED8A19");

})


$('#rechazado').click(function () {
    $('#estado').val('Rechazado')
    $('#estado').parent().addClass('focused')
    $("#estado").attr("disabled", true).css("background-color","#D75A4A");


})



var inputHoraInicio = document.getElementById('horai') ,
    inputHoraFin = document.getElementById('horaf')
inputHoraInicio.onfocusout = function (){ this.parentElement.classList.add('focused')}
inputHoraFin.onfocusout = function (){ this.parentElement.classList.add('focused')}

validationKeyup("form");
validationSelectChange("form");