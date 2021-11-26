main_route = '/portal_regularizacion'

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


$(document).ajaxStart(function () {
});

$(document).ajaxStop(function () {
    $.Toast.hideToast();
});

    $('.date').bootstrapMaterialDatePicker({
        format: 'D/MM/YYYY',
        clearButton: false,
        weekStart: 1,
        locale: 'es',
        time: false
    }).on('change', function (e, date) {
        // $(this).parent().addClass('focused');
        // eraseError(this)
        // $('#fecha').bootstrapMaterialDatePicker('setMinDate', date);
        console.log("fecha")

        cargar_registros()



    });


function color_input() {

    $('#estadoautorizacion').parent().addClass('focused')
    $("#estadoautorizacion").attr("disabled", true).css("background-color","#ffffff");
    document.getElementById("estadoautorizacion").style.color = "black";

    $('#estadoaprobacion').parent().addClass('focused')
    $("#estadoaprobacion").attr("disabled", true).css("background-color","#ffffff");
    document.getElementById("estadoaprobacion").style.color = "black";
}

$('#aceptado').click(function () {
    $('#estadoautorizacion').val('Aceptado')
    $('#estadoautorizacion').parent().addClass('focused')
    $("#estadoautorizacion").attr("disabled", true).css("background-color","#25AE88");
    document.getElementById("estadoautorizacion").style.color = "white";

})

$('#pendiente').click(function () {
    $('#estadoautorizacion').val('Pendiente')
    $('#estadoautorizacion').parent().addClass('focused')
    $("#estadoautorizacion").attr("disabled", true).css("background-color","#ED8A19");
    document.getElementById("estadoautorizacion").style.color = "white";

})

$('#rechazado').click(function () {
    $('#estadoautorizacion').val('Rechazado')
    $('#estadoautorizacion').parent().addClass('focused')
    $("#estadoautorizacion").attr("disabled", true).css("background-color","#D75A4A");
    document.getElementById("estadoautorizacion").style.color = "white";


})

$('#aceptado_aprobacion').click(function () {
    $('#estadoaprobacion').val('Aceptado')
    $('#estadoaprobacion').parent().addClass('focused')
    $("#estadoaprobacion").attr("disabled", true).css("background-color","#25AE88");
    document.getElementById("estadoaprobacion").style.color = "white";

})

$('#pendiente_aprobacion').click(function () {
    $('#estadoaprobacion').val('Pendiente')
    $('#estadoaprobacion').parent().addClass('focused')
    $("#estadoaprobacion").attr("disabled", true).css("background-color","#ED8A19");
    document.getElementById("estadoaprobacion").style.color = "white";

})

$('#rechazado_aprobacion').click(function () {
    $('#estadoaprobacion').val('Rechazado')
    $('#estadoaprobacion').parent().addClass('focused')
    $("#estadoaprobacion").attr("disabled", true).css("background-color","#D75A4A");
    document.getElementById("estadoaprobacion").style.color = "white";


})


$('#fkpersona').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar persona',
    title: 'Seleccione una persona'
})

function cargar_registros() {

    obj = JSON.stringify({
        'idPersona': $('#fkpersona').val(),
        'fecha': $('#fecha').val(),
        '_xsrf': getCookie("_xsrf")
    })

    ruta = "asistenciapersonal_listar_persona";
    //data.append('object', obj)
    //data.append('_xsrf',getCookie("_xsrf"))

    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: false
    }).done(function (response) {
        response = JSON.parse(response)
        console.log(response)

        // $('#fkresidente').html('');
        // var select = document.getElementById("fkresidente")

        for (var i = 0; i < Object.keys(response.response).length; i++) {

            // var option = document.createElement("OPTION");
            // option.innerHTML = response['response'][i]['fullname'];
            // option.value = response['response'][i]['id'];
            // select.appendChild(option);
            append_input_registro(response['response'][i]['id'])
            $('#id' + response['response'][i]['id']).val('')
            $('#fkasistencia' + response['response'][i]['id']).val(response['response'][i]['id'])
            $('#fecha' + response['response'][i]['id']).val(response['response'][i]['fecha'])
            $('#entrada' + response['response'][i]['id']).val(response['response'][i]['entrada'])
            $('#salida' + response['response'][i]['id']).val(response['response'][i]['salida'])

        }
        //$('#fkresidente').selectpicker('refresh');

    })

}

    function append_input_registro(id_in) {

        $('#registro_div').append(
        '<div class="row">\
            <div class="col-sm-1 hidden">\
                <div class="input-group">\
                <input  id="id'+id_in+'" class="form-control registro readonly txta-own">\
                </div>\
            </div>\
            <div class="col-sm-1">\
                <div  class="form-line">\
                    <input id="fkasistencia'+id_in+'" data-id="'+id_in+'" class="form-control registro txta-own">\
                </div>\
            </div>\
            <div class="col-sm-2">\
                <div  class="form-line">\
                    <input id="fecha'+id_in+'" data-id="'+id_in+'" class="form-control date txta-own">\
                </div>\
            </div>\
            <div class="col-sm-1">\
                <div  class="form-line">\
                    <input id="entrada'+id_in+'" data-id="'+id_in+'" class="form-control hr txta-own">\
                </div>\
            </div>\
            <div class="col-md-1 ">\
                <input id="m_e'+id_in+'" type="checkbox" class="module chk-col-deep-purple registro" data-id="1" >\
                <label for="m_e'+id_in+'"></label>\
            </div>\
            <div class="col-sm-1">\
                <div  class="form-line">\
                    <input id="salida'+id_in+'" data-id="'+id_in+'" class="form-control hr txta-own">\
                </div>\
            </div>\
            <div class="col-md-1 ">\
                <input id="m_s'+id_in+'" type="checkbox" class="module chk-col-deep-purple registro" data-id="1" >\
                <label for="m_s'+id_in+'"></label>\
            </div>\
            <div class="col-sm-3">\
                <div  class="form-line">\
                    <input id="motivo'+id_in+'" data-id="'+id_in+'" class="form-control registro txta-own">\
                </div>\
            </div>\
            <div class="col-sm-1">\
                <button type="button" class="btn bg-red waves-effect white-own clear_registro" title="Eliminar">\
                    <i class="material-icons">clear</i>\
                </button>\
            </div>\
        </div>'
    )

        $('.clear_registro').last().click(function () {
            $(this).parent().parent().remove()
        })

        $('.show-tick').selectpicker()
        $('.date').bootstrapMaterialDatePicker({
            format: 'D/MM/YYYY',
            clearButton: false,
            weekStart: 1,
            locale: 'es',
            time: false
        }).on('change', function (e, date) {
            $(this).parent().addClass('focused');
            eraseError(this)
            // $('#fecha').bootstrapMaterialDatePicker('setMinDate', date);
        });

        $(".hr").inputmask("h:s",{ "placeholder": "__/__" });
    }

    function get_registros() {
        objeto = []
        objeto_inputs = $('.registro')


        for (i = 0; i < objeto_inputs.length; i += 5) {
            h0 = objeto_inputs[i].value
            h1 = objeto_inputs[i + 1].value
            h2 = objeto_inputs[i + 2].checked
            h3 = objeto_inputs[i + 3].checked
            h4 = objeto_inputs[i + 4].value


            objeto.push((function add_invitado(h0, h1, h2,h3,h4) {

                if (h0 ==''){
                    return {
                        'fkasistencia': h1,
                        'entrada': h2,
                        'salida': h3,
                        'motivo': h4

                    }

                }else{
                    return {
                    'id':h0,
                    'fkasistencia': h1,
                    'entrada': h2,
                    'salida': h3,
                    'motivo': h4
                    }
                }


            })(
                h0,
                h1,
                h2,
                h3,
                h4))
        }

        return objeto
    }

    $('#agregar_registro').click(function () {

        append_input_registro('')
    })

///////////////////////////////////////////////////////////////////////////////////////////////////////////////


$('#new').click(function () {

    $('#fkpersona').val($('#idpersona').val())
    $('#fkpersona').selectpicker('refresh')
    $('#motivo').val('')

    $('#estadoautorizacion').val('Pendiente')
    $('#estadoaprobacion').val('Pendiente')
    
        if ($('#rol').val() == "ADMINISTRADOR"){
        document.getElementById('fkpersona').disabled  = false;
    }else{
        document.getElementById('fkpersona').disabled  = true;
    }

    color_input()

    verif_inputs('')
    $('#id_div').hide()
    $('#insert').show()
    $('#update').hide()
    $('#autorizacion').hide()
    $('#aprobacion').hide()
    $('#respuesta_autorizacion').hide()
    $('#respuesta_aprobacion').hide()
    validationInputSelects("form")
    $('#form').modal('show')
})


$('#insert').click(function () {
    notvalid = validationInputSelectsWithReturn("form");
    if (notvalid === false) {
        objeto = JSON.stringify({
            'fkpersona': $('#fkpersona').val(),
            'regularizaciondetalle': get_registros()
        })
        ajax_call('portal_regularizacion_insert', {
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

        ajax_call_get('portal_regularizacion_update', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            $('#id').val(self.id)
            $('#fkpersona').val(self.fkpersona)
            $('#fkpersona').selectpicker('refresh')

            $('#estadoautorizacion').val(self.estadoautorizacion)
            $('#estadoaprobacion').val(self.estadoaprobacion)

            $('#registro_div').empty()

            for (i in self.regularizaciondetalle) {

                append_input_registro(self.regularizaciondetalle[i]['id'])

                $('#id' + self.regularizaciondetalle[i]['id']).val(self.regularizaciondetalle[i]['id'])
                $('#fkasistencia' + self.regularizaciondetalle[i]['id']).val(self.regularizaciondetalle[i]['fkasistencia'])
                $('#fecha' + self.regularizaciondetalle[i]['id']).val(self.regularizaciondetalle[i]['asistencia']['fecha'])
                $('#entrada' + self.regularizaciondetalle[i]['id']).val(self.regularizaciondetalle[i]['asistencia']['entrada'])
                $('#salida' + self.regularizaciondetalle[i]['id']).val(self.regularizaciondetalle[i]['asistencia']['salida'])
                $('#m_e' + self.regularizaciondetalle[i]['id']).prop('checked', self.regularizaciondetalle[i]['entrada'])
                $('#m_s' + self.regularizaciondetalle[i]['id']).prop('checked', self.regularizaciondetalle[i]['salida'])
                $('#motivo' + self.regularizaciondetalle[i]['id']).val(self.regularizaciondetalle[i]['motivo'])


            }

            color_input()

            clean_form()
            verif_inputs('')
            $('#id_div').hide()
            $('#insert').hide()
            $('#update').show()
            $('#respuesta_autorizacion').hide()
            $('#respuesta_aprobacion').hide()
            $('#autorizacion').hide()
            $('#aprobacion').hide()
            $('#form').modal('show')
        })
    })

    $('.autorizacion').click(function () {
        obj = JSON.stringify({
            'id': parseInt(JSON.parse($(this).attr('data-json')))
        })
        ajax_call_get('portal_regularizacion_autorizacion', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            console.log(self)
            $('#id').val(self.id)
            $('#fkpersona').val(self.fkpersona)
            $('#fkpersona').selectpicker('refresh')

            $('#respuestaautorizacion').val(self.respuestaautorizacion)
            $('#respuestaaprobacion').val(self.respuestaaprobacion)

            $('#estadoautorizacion').val(self.estadoautorizacion)
            $('#estadoaprobacion').val(self.estadoaprobacion)

            $('#registro_div').empty()

            for (i in self.regularizaciondetalle) {

                append_input_registro(self.regularizaciondetalle[i]['id'])

                $('#id' + self.regularizaciondetalle[i]['id']).val(self.regularizaciondetalle[i]['id'])
                $('#fkasistencia' + self.regularizaciondetalle[i]['id']).val(self.regularizaciondetalle[i]['fkasistencia'])
                $('#fecha' + self.regularizaciondetalle[i]['id']).val(self.regularizaciondetalle[i]['asistencia']['fecha'])
                $('#entrada' + self.regularizaciondetalle[i]['id']).val(self.regularizaciondetalle[i]['asistencia']['entrada'])
                $('#salida' + self.regularizaciondetalle[i]['id']).val(self.regularizaciondetalle[i]['asistencia']['salida'])
                $('#m_e' + self.regularizaciondetalle[i]['id']).prop('checked', self.regularizaciondetalle[i]['entrada'])
                $('#m_s' + self.regularizaciondetalle[i]['id']).prop('checked', self.regularizaciondetalle[i]['salida'])
                $('#motivo' + self.regularizaciondetalle[i]['id']).val(self.regularizaciondetalle[i]['motivo'])


            }

            color_input()

            clean_form()
            verif_inputs('')
            $('#id_div').hide()
            $('#insert').hide()
            $('#update').hide()
            $('#respuesta_autorizacion').show()
            $('#autorizacion').show()
            $('#respuesta_aprobacion').hide()
            $('#aprobacion').hide()

            $('#form').modal('show')
        })
    })

    $('.aprobacion').click(function () {
        obj = JSON.stringify({
            'id': parseInt(JSON.parse($(this).attr('data-json')))
        })
        ajax_call_get('portal_regularizacion_aprobacion', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            $('#id').val(self.id)

            $('#fkpersona').val(self.fkpersona)
            $('#fkpersona').selectpicker('refresh')

            $('#respuestaautorizacion').val(self.respuestaautorizacion)
            $('#respuestaaprobacion').val(self.respuestaaprobacion)

            $('#estadoautorizacion').val(self.estadoautorizacion)
            $('#estadoaprobacion').val(self.estadoaprobacion)

            $('#registro_div').empty()

            for (i in self.regularizaciondetalle) {

                append_input_registro(self.regularizaciondetalle[i]['id'])

                $('#id' + self.regularizaciondetalle[i]['id']).val(self.regularizaciondetalle[i]['id'])
                $('#fkasistencia' + self.regularizaciondetalle[i]['id']).val(self.regularizaciondetalle[i]['fkasistencia'])
                $('#fecha' + self.regularizaciondetalle[i]['id']).val(self.regularizaciondetalle[i]['asistencia']['fecha'])
                $('#entrada' + self.regularizaciondetalle[i]['id']).val(self.regularizaciondetalle[i]['asistencia']['entrada'])
                $('#salida' + self.regularizaciondetalle[i]['id']).val(self.regularizaciondetalle[i]['asistencia']['salida'])
                $('#m_e' + self.regularizaciondetalle[i]['id']).prop('checked', self.regularizaciondetalle[i]['entrada'])
                $('#m_s' + self.regularizaciondetalle[i]['id']).prop('checked', self.regularizaciondetalle[i]['salida'])
                $('#motivo' + self.regularizaciondetalle[i]['id']).val(self.regularizaciondetalle[i]['motivo'])


            }

            color_input()

            clean_form()
            verif_inputs('')
            $('#id_div').hide()
            $('#insert').hide()
            $('#update').hide()
            $('#respuesta_autorizacion').hide()
            $('#respuesta_aprobacion').show()
            $('#autorizacion').hide()
            $('#aprobacion').show()
            $('#form').modal('show')
        })
    })

    $('.imprimir').click(function () {
        obj = JSON.stringify({
            'id': parseInt(JSON.parse($(this).attr('data-json')))
        })
        $.ajax({
            method: "POST",
            url: '/portal_regularizacion_imprimir',
            data: {object: obj, _xsrf: getCookie("_xsrf")}
        }).done(function (response) {
            dictionary = JSON.parse(response)
            dictionary = dictionary.response
            servidor = ((location.href.split('/'))[0]) + '//' + (location.href.split('/'))[2];
            url = servidor + dictionary;

            window.open(url)
        })
    })

}

attach_edit()


$('#update').click(function () {
    notvalid = validationInputSelectsWithReturn("form");
    if (notvalid === false) {
        objeto = JSON.stringify({
            'id': parseInt($('#id').val()),
            'fkpersona': $('#fkpersona').val(),
            'motivo': $('#motivo').val(),
            'regularizaciondetalle': get_registros()
        })
        ajax_call('portal_regularizacion_update', {
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

$('#autorizacion').click(function () {
    if (!validationInputSelects("form")) {
        objeto = JSON.stringify({
            'id': parseInt($('#id').val()),
            'estadoautorizacion': $('#estadoautorizacion').val(),
            'respuestaautorizacion': $('#respuestaautorizacion').val()
        })
        ajax_call('portal_regularizacion_autorizacion', {
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

$('#aprobacion').click(function () {
    if (!validationInputSelects("form")) {
        objeto = JSON.stringify({
            'id': parseInt($('#id').val()),
            'estadoaprobacion': $('#estadoaprobacion').val(),
            'respuestaaprobacion': $('#respuestaaprobacion').val()
        })
        ajax_call('portal_regularizacion_aprobacion', {
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


$('.delete').click(function (e) {
    e.preventDefault()
    cb_delete = this
    b = $(this).prop('checked')
    if (!b) {
        cb_title = "¿Está seguro de que desea dar de baja la regularizacion?"

    } else {
        cb_title = "¿Está seguro de que desea dar de alta la regularizacion?"
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
        ajax_call('portal_regularizacion_delete', {
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

validationKeyup("form");
validationSelectChange("form");