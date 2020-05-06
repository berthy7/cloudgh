main_route = '/ausencia'

$(document).ready(function () {
    $('#data_table').DataTable();
});

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
            'fktipoausencia': $('#fktipoausencia').val(),
            'fkpersona': $('#fkpersona').val(),
            'descripcion': $('#descripcion').val(),
            'fechai': $('#fechai').val(),
            'horai': $('#horai').val(),
            'fechaf': $('#fechaf').val(),
            'horaf': $('#horaf').val(),
            'estado': $('#estado').val()

        })

        objeto_verificar = JSON.stringify({
            'fkpersona': $('#fkpersona').val(),
            'fechai': $('#fechai').val(),
            'fechaf': $('#fechaf').val()

        })

        ajax_call_post("v_personal_disponible", {
            _xsrf: getCookie("_xsrf"),
            object: objeto_verificar
            }, function (response) {
                if(response.success === true){

                    ajax_call_ausencia('ausencia_insert',{
                        object: objeto,
                        _xsrf: getCookie("_xsrf")
                    },null, function () {
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
        ajax_call_get('ausencia_update', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            $('#id').val(self.id)
            $('#fktipoausencia').val(self.fktipoausencia)
            $('#fktipoausencia').selectpicker('refresh')
            $('#fkpersona').val(self.fkpersona)
            $('#fkpersona').selectpicker('refresh')
            $('#descripcion').val(self.descripcion)
            $('#fechai').val(self.fechai)
            $('#horai').val(self.horai)
            $('#fechaf').val(self.fechaf)
            $('#horaf').val(self.horaf)
            $('#estado').val(self.estado)
            $('#estado').selectpicker('refresh')

            //clean_form()
            verif_inputs('')
            validationInputSelects("form")
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
            'fktipoausencia': $('#fktipoausencia').val(),
            'fkpersona': $('#fkpersona').val(),
            'descripcion': $('#descripcion').val(),
            'fechai': $('#fechai').val(),
            'horai': $('#horai').val(),
            'fechaf': $('#fechaf').val(),
            'horaf': $('#horaf').val(),
            'estado': $('#estado').val()
        })
        ajax_call('ausencia_update', {
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
        ajax_call('ausencia_delete', {
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

var inputHoraInicio = document.getElementById('horai') ,
    inputHoraFin = document.getElementById('horaf')
inputHoraInicio.onfocusout = function (){ this.parentElement.classList.add('focused')}
inputHoraFin.onfocusout = function (){ this.parentElement.classList.add('focused')}

function ajax_call_ausencia(url, data, render, callback) {
    $.ajax({
        method: "POST",
        url: url,
        data: data,
        async: false
    }).done(function (response) {

        response = JSON.parse(response)
        exito = response.success;
        response = response.response;
        //si exito es verdarero, se inserto ausencia
        if (exito==true || exito=="true" ){
            var exito;
            exito = () => {
                swal(
                    'Operación exitosa.',
                    'Ausencia ingresada correctamente',
                    'success'
                )
            }
            exito();

        } else if (response.indexOf('None')>-1){
            swal(
                'Error.',
                'No tiene un superior asignado',
                'error'
            )
        }
        if(callback != null){
            callback(response)
        }
    })
}


validationKeyup("form");
validationSelectChange("form");