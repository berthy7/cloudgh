main_route = '/turno'

$(document).ready(function () {
    $('#data_table').DataTable();
});

$(document).ajaxStart(function () { });

$(document).ajaxStop(function () {
    $.Toast.hideToast();
});




function agregar_turno(id_in) {
    $('#turno_div').append(
        '<div class="row">\
            <div class="col-md-2" hidden>\
                <div class="form-group form-float">\
                    <div class="form-line">\
                        <input id="id'+id_in+'" data-id="'+id_in+'" class="form-control id horas" readonly>\
                        <label class="form-label">Id</label>\
                    </div>\
                </div>\
            </div>\
            <div class="col-md-3">\
                <b>Entrada min.</b>\
                <div class="input-group">\
                    <span class="input-group-addon"><i class="material-icons">access_time</i></span>\
                    <div class="form-line"><input id="entrada_min_'+id_in+'" name="Entrada Mínima" type="text" class="form-control horas hr" placeholder="Ex: 23:59" tabindex=2 required></div>\
                </div>\
                <b>Salida min.</b>\
                <div class="input-group">\
                    <span class="input-group-addon"><i class="material-icons">access_time</i></span>\
                    <div class="form-line"><input id="salida_min_'+id_in+'" name="Salida Mínima" type="text" class="form-control horas hr" placeholder="Ex: 23:59" tabindex=5 required></div>\
                </div>\
            </div>\
            <div class="col-md-3">\
                <b>Entrada</b>\
                <div class="input-group">\
                    <span class="input-group-addon"><i class="material-icons">access_time</i></span>\
                    <div class="form-line"><input id="entrada_'+id_in+'" name="Entrada" type="text" class="form-control horas hr" placeholder="Ex: 23:59" tabindex=3 required></div>\
                </div>\
                <b>Salida</b>\
                <div class="input-group">\
                    <span class="input-group-addon"><i class="material-icons">access_time</i></span>\
                    <div class="form-line"><input id="salida_'+id_in+'" name="Salida" type="text" class="form-control horas hr" placeholder="Ex: 23:59" tabindex=6 required></div>\
                </div>\
            </div>\
            <div class="col-md-3">\
                <b>Entrada max.</b>\
                <div class="input-group">\
                    <span class="input-group-addon"><i class="material-icons">access_time</i></span>\
                    <div class="form-line"><input id="entrada_max_'+id_in+'" name="Entrada Máxima" type="text" class="form-control horas hr" placeholder="Ex: 23:59" tabindex=4 required></div>\
                </div>\
                <b>Salida max.</b>\
                <div class="input-group">\
                    <span class="input-group-addon"><i class="material-icons">access_time</i></span>\
                    <div class="form-line"><input id="salida_max_'+id_in+'" name="Salida Máxima" type="text" class="form-control horas hr" placeholder="Ex: 23:59" tabindex=7 required></div>\
                </div>\
            </div>\
            <div class="col-md-3">\
                <button type="button" class="btn bg-deep-purple waves-effect borrar_turno">\
                    <i class="material-icons">clear</i>\
                </button>\
            </div>\
        </div>'
    )
    $('.borrar_turno').last().click(function () {
        $(this).parent().parent().remove()
    })

    $(".hr").inputmask("h:s",{ "placeholder": "__/__" });
}

$('#nuevo_turno').click(function () {
    agregar_turno('')
})

function obtener_turno() {
    objeto = []
    objeto_clase = $('.horas')

    console.log(objeto_clase)

    for(i=0;i<objeto_clase.length;i+=7){
        h0 = obtener_segundos(objeto_clase[i].value)
        h1= obtener_segundos(objeto_clase[i+1].value)
        h2 = obtener_segundos(objeto_clase[i+3].value)
        h3 = obtener_segundos(objeto_clase[i+5].value)
        h4 = obtener_segundos(objeto_clase[i+2].value)
        h5 = obtener_segundos(objeto_clase[i+4].value)
        h6 = obtener_segundos(objeto_clase[i+6].value)

        objeto.push((function add_objeto(h0, h1, h2, h3, h4, h5,h6) {
            if (h0 ==''){
                return {
                    'entrada': h3,
                    'salida': h4,
                    'entradamin': h1,
                    'entradamax': h5,
                    'salidamin': h2,
                    'salidamax': h6
                }
            }else{
                return {
                    'id': h0,
                        'entrada': h3,
                        'salida': h4,
                        'entradamin': h1,
                        'entradamax': h5,
                        'salidamin': h2,
                        'salidamax': h6
                    }
            }
        })(
            objeto_clase[i].value,
            objeto_clase[i+1].value,
            objeto_clase[i+2].value,
            objeto_clase[i+3].value,
            objeto_clase[i+4].value,
            objeto_clase[i+5].value,
            objeto_clase[i+6].value)
        )
    }
    return objeto
}

function obtener_segundos(hora) {
    hm = hora.split(':')
    sec = (parseInt(hm[0])*3600) + (parseInt(hm[1])*60)
    return sec
}


$('#new').click(function () {
     $('#id').val('')
    $('#nombre').val('')
    $('#turno_div').empty()
    agregar_turno('')

    verif_inputs('')
    $('#id_div').hide()
    $('#insert').show()
    $('#update').hide()
    validationInputSelects("form")
    $('#form').modal('show')
})


$('#insert').click(function () {
    hora = validarLongitudHora("turno_div");
    // horaValida = validarHorarios("turno_div");
    if (hora===true) {
        notvalid = validationInputSelectsWithReturn("form");
        if (notvalid===false) {
            conflictoHorario = validarConflictoHorarios("turno_div");
            if(conflictoHorario===false){
                objeto = JSON.stringify({
                    'nombre': $('#nombre').val(),
                    'hora': obtener_turno()
                })

                ajax_call('turno_insert', {
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
                    'Error de datos.',
                    conflictoHorario,
                    'error'
                     )
            }

        }else{
            swal(
            'Error de datos.',
            notvalid,
            'error'
             )
        }

    } else {
        swal(
            'Error de datos.',
            'Ingrese la hora correctamente',
            'error'
        )
    }
})

$('#sms').click(function () {
    console.log("h")
     $('#id').val('')
    $('#telefeno').val('')
    $('#texto').empty()


    verif_inputs('')
    $('#insert-sms').show()

    validationInputSelects("form")
    $('#form-sms').modal('show')
})

$('#insert_sms').click(function () {

    objeto = JSON.stringify({
        'telefono': $('#telefono').val(),
        'texto': $('#texto').val()
    })

    ajax_call('turno_sms', {
        object: objeto,
        _xsrf: getCookie("_xsrf")
    }, null, function () {
        setTimeout(function () {
            window.location = main_route
        }, 2000);
    })
    $('#form-sms').modal('hide')

})


function attach_edit() {
    $('.edit').click(function () {
        obj = JSON.stringify({
            'id': parseInt(JSON.parse($(this).attr('data-json')))
        })

        ajax_call_get('turno_update', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            console.log(self)
            $('#id').val(self.id)
            $('#nombre').val(self.nombre)

            $('#turno_div').empty()

            for(i in self.hora){
                aux0 = self.hora[i].id
                aux1 = self.hora[i].entrada
                aux2= self.hora[i].salida
                aux3 = self.hora[i].entradamin
                aux4 = self.hora[i].entradamax
                aux5 = self.hora[i].salidamin
                aux6 = self.hora[i].salidamax

                agregar_turno(aux0)
                $('#id'+aux0).val(aux0)
                $('#entrada_'+aux0).val(aux1)
                $('#salida_'+aux0).val(aux2)
                $('#entrada_min_'+aux0).val(aux3)
                $('#entrada_max_'+aux0).val(aux4)
                $('#salida_min_'+aux0).val(aux5)
                $('#salida_max_'+aux0).val(aux6)
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
        objeto = JSON.stringify({
            'id': parseInt($('#id').val()),
            'nombre': $('#nombre').val(),
            'hora': obtener_turno()
        })

        ajax_call('turno_update', {
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
        title: "¿Desea dar de baja el turno?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#1565c0",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    }).then(function () {
        ajax_call('turno_delete', {
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