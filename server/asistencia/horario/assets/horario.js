main_route = '/horario'

$(document).ready(function () {
    $('#data_table').DataTable();
});

$(document).ajaxStart(function () { });

$(document).ajaxStop(function () {
    $.Toast.hideToast();
});

function get_details(schedule_id) {
    aux = $('select.detail')
    details_dict = {}
    for(i in aux){
        (function aux1(day_id) {
            if(day_id > 0){
                schedule_day = aux[i].id
                if(!(day_id in details_dict)){
                    details_dict[day_id] = {
                        'fkdia': day_id,
                        'lunes': false,
                        'martes': false,
                        'miercoles': false,
                        'jueves': false,
                        'viernes': false,
                        'sabado': false,
                        'domingo': false
                    }
                    if(schedule_id != null){
                        details_dict[day_id]['fksemanal'] = schedule_id
                    }
                }
                details_dict[day_id][schedule_day] = true
            }
        })(aux[i].value)
    }
    details = []
    for(j in details_dict){
        details.push(details_dict[j])
    }
    return details
}


$('#new').click(function () {
    $('#id').val('')
    $('#nombre').val('')
    $('select.detail').val(0)
    $('select.detail').selectpicker('render')

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
    if (notvalid===false) {
        objeto = JSON.stringify({
            'nombre': $('#nombre').val(),
            'semanaldetalle': get_details()
        })

        ajax_call('horario_insert', {
            object: objeto,
            _xsrf: getCookie("_xsrf")
        }, null, function () {
            setTimeout(function () {
                window.location = main_route
            }, 2000);
        })
        $('#form').modal('hide')
    }
    else {
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

        ajax_call_get('horario_update', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            $('#id').val(self.id)
            $('#nombre').val(self.nombre)
            $('select.detail').val(0)
            $('select.detail').selectpicker('render')

            for(i in self.semanaldetalle){
                for(j in self.semanaldetalle[i]){
                    if(self.semanaldetalle[i][j] == true){
                        $('#'+j).val(self.semanaldetalle[i].fkdia)
                        $('#'+j).selectpicker('render')
                    }
                }
            }

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
        semanal_id = parseInt($('#id').val())
        objeto = JSON.stringify({
            'id': semanal_id,
            'nombre': $('#nombre').val(),
            'semanaldetalle': get_details(semanal_id)
        })

        ajax_call('horario_update', {
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
        title: "¿Desea dar de baja el examen?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#1565c0",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    }).then(function () {
        ajax_call('horario_delete', {
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