main_route = '/portal_vacacion'

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

var fechahoy = new Date();
var hoy = fechahoy.getDate()+"/"+(fechahoy.getMonth()+1) +"/"+fechahoy.getFullYear()
var id_gv = 0

$(".hr").inputmask("h:s",{ "placeholder": "__/__" });

document.getElementById("fechai").value=hoy
// document.getElementById("fechaf").value=hoy

$('.show-tick').selectpicker()

$('.dd').nestable({
    group:'categories',
    maxDepth:0,
    reject: [{
        rule: function () {
            // The this object refers to dragRootEl i.e. the dragged element.
            // The drag action is cancelled if this function returns true
            var ils = $(this).find('>ol.dd-list > li.dd-item');
            for (var i = 0; i < ils.length; i++) {
                var datatype = $(ils[i]).data('type');
                if (datatype === 'child')
                    return true;
            }
            return false;
        },
        action: function (nestable) {
            // This optional function defines what to do when such a rule applies. The this object still refers to the dragged element,
            // and nestable is, well, the nestable root element
            alert('Can not move this item to the root');
        }
    }]
});

$('.module').click(function () {
    var checked = $(this).prop('checked')
    //$('.module').prop('checked', false)
    empresa_id = null
    sucursal_id = null
    gerencia_id = null
    grupo_id = null
    emp_id = null
    if ($(this).hasClass('employee')){
        emp_id = parseInt($(this).attr('data-id'))
    } else {
        if ($(this).hasClass('grupo')){
            grupo_id = parseInt($(this).attr('data-id'))
            gerencia_id = parseInt($(this).attr('data-ger'))
            sucursal_id = parseInt($(this).attr('data-suc'))
            empresa_id = parseInt($(this).attr('data-empr'))
        } else {
            if ($(this).hasClass('gerencia')){
                gerencia_id = parseInt($(this).attr('data-id'))
                sucursal_id = parseInt($(this).attr('data-suc'))
                empresa_id = parseInt($(this).attr('data-empr'))
            }else {
                if($(this).hasClass('sucursal')){
                    sucursal_id = parseInt($(this).attr('data-id'))
                    empresa_id = parseInt($(this).attr('data-empr'))
                }else {
                    if($(this).hasClass('empresa')){
                        empresa_id_id = parseInt($(this).attr('data-id'))
                    }
                }
            }
        }
    }
    $(this).prop('checked', checked)
    $(this).parent().next().find('.module').prop('checked', $(this).prop('checked'))
    analizar($(this).parent().parent().closest('.dd-list').prev().find('.module'))
})

function analizar(parent) {
    children = $(parent).parent().next().find('.module:checked')
    //console.log(children.length)
    $(parent).prop('checked', (children.length > 0))
    grand_parent = $(parent).parent().parent().closest('.dd-list').prev().find('.module')
    //console.log(grand_parent.length)
    if (grand_parent.length > 0){
        analizar(grand_parent)
    }
}

function color_input() {

    $('#estadoautorizacion').parent().addClass('focused')
    $("#estadoautorizacion").attr("disabled", true).css("background-color","#ffffff");
    document.getElementById("estadoautorizacion").style.color = "black";

    $('#estadoaprobacion').parent().addClass('focused')
    $("#estadoaprobacion").attr("disabled", true).css("background-color","#ffffff");
    document.getElementById("estadoaprobacion").style.color = "black";
}

$('#fkpersona').change(function () {
    obtener_dias_vacacion($('#fkpersona').val())
});

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

function obtener_dias_vacacion(idpersona) {
    obj = JSON.stringify({
        'idpersona': idpersona,
        '_xsrf': getCookie("_xsrf")
    })

    ajax_call_post("v_personal_obtener",{
    _xsrf: getCookie("_xsrf"),
    object: obj
    }, function (response) {
        console.log(response.response)
        $('#dias_vacacion').val(response.response)
    })
}


$('#personal').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar Personal',
    title: 'Seleccione una persona.'
})

$('#personal').change(function () {
    obj = JSON.stringify({
        'id': parseInt(JSON.parse($('#personal').val())),
        '_xsrf': getCookie("_xsrf")
    })

    ruta = "persona_obtener_id";

    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: false
    }).done(function (response) {
        response = JSON.parse(response)
        append_input_personal('')
        var id_nombres = ''
        $("input.nombres").each(function() {
            id_nombres  = $(this).prop('id');
        });
        var id_id = ''
        $("input.idnombres").each(function() {
            id_id = $(this).prop('id');
        });


        $('#' + id_id ).val(response.response.id)
        $('#' + id_id ).parent().addClass('focused')
        $('#' + id_nombres ).val(response.response.fullname)
        $('#' + id_nombres ).parent().addClass('focused')


    })

    $('#personal').val('')
    $('#personal').selectpicker('refresh')

});

function append_input_personal(id_in) {
    if(id_in === ''){
        id_gv++;
        id_in = id_gv;
    }
    $('#personal_div').append(
        '<div class="row">\
            <div class="col-md-1 hidden">\
                <div class="input-group">\
                <input  id="id'+id_in+'" class="form-control idnombres personal readonly">\
                </div>\
            </div>\
            <div class="col-md-8 p-t-own">\
                <div class="form-group form-float">\
                    <div id="nombresDIV" class="form-line">\
                        <input id="nombres'+id_in+'" data-id="'+id_in+'" class="form-control nombres">\
                        <label class="form-label">Nombre Completo</label>\
                    </div>\
                </div>\
            </div>\
            <div class="col-sm-2">\
                <button type="button" class="btn bg-red waves-effect clear_personal" title="Eliminar">\
                    <i class="material-icons">clear</i>\
                </button>\
            </div>\
        </div>'
    )

    $('.clear_personal').last().click(function () {
        $(this).parent().parent().remove()
    })

    $('.nombres').click(function () {
        $(this).parent().addClass('focused');
        current_input = $(this).prop('id');
    })

    $('.idnombres').click(function () {
        $(this).parent().addClass('focused');
        current_input = $(this).prop('id');
    })

}

function obtener_personas_arbol() {
    aux = []
    $('.employee:checked').each(function () {
        var a = parseInt($(this).attr('data-id'))

        aux.push((function add(a) {

            return a

        })(a))
    })
    return aux
}

function obtener_personas() {
        objeto = []
        objeto_inputs = $('.personal')

        for (i = 0; i < objeto_inputs.length; i += 1) {
            h0 = parseInt(objeto_inputs[i].value)

            objeto.push((function add_objeto(h0) {

                    return h0

            })(
                h0))
        }
        return objeto
    }

function append_input_sin_vacacion(id_in) {

    $('#sin_vacacion_div').append(
        '<div class="row">\
            <div class="col-md-1" hidden>\
                <div class="input-group">\
                <input  id="id_sin_vacacion'+id_in+'" class="form-control sin_vacacion  readonly">\
                </div>\
            </div>\
            <div class="col-md-8">\
                <div class="form-group form-float">\
                    <div  class="form-line">\
                        <input id="nombre_sin_vacacion'+id_in+'" data-id="'+id_in+'" class="form-control ">\
                    </div>\
                </div>\
            </div>\
            <div class="col-md-2 ">\
                <input id="b_sin_vacacion'+id_in+'" type="checkbox" class="regular-checkbox big-checkbox sin_vacacion" data-id="1" >\
                <label for="b_sin_vacacion'+id_in+'"></label>\
            </div>\
        </div>'
    )


}

function obtener_sin_vacacion() {
        objeto = []
        objeto_inputs = $('.sin_vacacion')

        for(i=0;i<objeto_inputs.length;i+=2){
            h0 = parseInt(objeto_inputs[i].value)
            h1 = objeto_inputs[i+1].checked

            objeto.push((function add_hours(h0,h1) {
                
                    return {
                    'id':h0,
                    'estado': h1
                    }
           

            })(
                    h0,
                    h1))
        }
        return objeto
    }


$('#fktipovacacion').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar vacacion',
    title: 'Seleccione el tipo de vacacion'
})

$('#fkpersona').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar persona',
    title: 'Seleccione una persona'
})

$('#boton_dias').click(function () {
    objeto_verificar = JSON.stringify({
        'dias': $('#dias').val(),
        'fechai': $('#fechai').val(),
    })

    if ($('#dias').val() !== '') {
        ajax_call_post("v_personal_dias", {
            _xsrf: getCookie("_xsrf"),
            object: objeto_verificar
        }, function (response) {
            if(response.success === true){
                console.log(response)

                $('#fechaf').val(response.response)
            } else {
                swal('No se pudo procesar.', response.message, response.tipo)
            }
        });
    }
    else swal('No se pudo calcular', 'Por favor, ingrese un valor en el campo "días"', 'warning');
});
$('#fktipovacacion').change(function () {

    cambio_tipo_vacacion(parseInt(JSON.parse($('#fktipovacacion').val())))

});

function cambio_tipo_vacacion(tipovacacion) {

        if(tipovacacion == 1 || tipovacacion == 4){
        $('#row_fkpersona').show()
        $('#div_medio_dia').hide()
        $('#row_colectivo').hide()
        $('#fkpersona').prop("required", true);
        $('#sin_vacacion').hide()
        $('#sin_vacacion_div').empty()
        $('.hora_i_f').hide()

    }else if(tipovacacion == 2){
        $('#row_fkpersona').show()
        $('#div_medio_dia').show()
        $('#row_colectivo').hide()
        $('#fkpersona').prop("required", true);
        $('#sin_vacacion').hide()
        $('#sin_vacacion_div').empty()
        $('.hora_i_f').show()
    }else if(tipovacacion == 3){
        $('#row_fkpersona').hide()
        $('#div_medio_dia').hide()
        $('#row_colectivo').show()
        $('#fkpersona').removeAttr("required");
        $('#sin_vacacion').hide()
        $('#sin_vacacion_div').empty()
        $('.hora_i_f').hide()
    }
}


$('#new').click(function () {
    $('#fktipovacacion').val('')
    $('#fktipovacacion').selectpicker('refresh')
    $('#fkpersona').val($('#idpersona').val())
    $('#fkpersona').selectpicker('refresh')
    $('#descripcion').val('')
    $('#fechai').val('')
    $('#fechaf').val('')
    $('#fechaf').parent().addClass('focused');
    document.getElementById("fechai").value=hoy
    // document.getElementById("fechaf").value=hoy
    $('#estadoautorizacion').val('Pendiente')
    $('#estadoaprobacion').val('Pendiente')

    color_input()
     obtener_dias_vacacion($('#fkpersona').val())


    $('#sin_vacacion_div').empty()

    $('#id_div').hide()
    $('#insert').show()
    $('#update').hide()
    $('#autorizacion').hide()
    $('#aprobacion').hide()
    $('#respuesta_autorizacion').hide()
    $('#respuesta_aprobacion').hide()
    $('#div_medio_dia').hide()
    verif_inputs('')
    validationInputSelects("form")
    $('#form').modal('show')
})


$('#insert').click(function () {
    notvalid = validationInputSelectsWithReturn("form");
    if (notvalid===false) {

        objeto_verificar = JSON.stringify({
            'dias': $('#dias').val(),
            'fechai': $('#fechai').val(),
        })


        if ($('#fechaf').val() == '') {
            ajax_call_post("v_personal_dias", {
                _xsrf: getCookie("_xsrf"),
                object: objeto_verificar
            }, function (response) {
                if(response.success === true) {
                    console.log("repuesta fecha f ")

                    $('#fechaf').val(response.response)
                    $('#dtfin').calendar('setDate', str_to_date(response.response))
                }
            });
        }

        
        objeto_verificar = JSON.stringify({
            'fktipovacacion': $('#fktipovacacion').val(),
            'fkpersona': $('#fkpersona').val(),
            'descripcion': $('#descripcion').val(),
            'fechai': $('#fechai').val(),
            'fechaf': $('#fechaf').val(),
            'horai': $('#horai').val(),
            'horaf': $('#horaf').val(),
            'dias': $('#dias').val(),
            'mañana':document.getElementById('mañana').checked,
            'tarde':document.getElementById('tarde').checked,
            'personas_arbol': obtener_personas_arbol(),
            'personas': obtener_personas(),
            'sin_vacacion': obtener_sin_vacacion(),
        })

        ajax_call_post("v_personal_disponible", {
            _xsrf: getCookie("_xsrf"),
            object: objeto_verificar
            }, function (response) {
                console.log(response)
                if(response.success === true){

                    ajax_call_post("portal_vacacion_insert",{
                    _xsrf: getCookie("_xsrf"),
                    object: objeto_verificar
                    }, function (response) {

                        console.log('salida')
                        setTimeout(function () {
                            window.location = main_route
                        }, 2000);
                    })
                    $('#form').modal('hide')

                }else{

                    swal(
                        'No se pudo procesar.',
                        response.message,
                        response.tipo 
                    )
                    console.log(response)
                    if (response.response != "no"){
                        $('#sin_vacacion').show()
                        for (persona in response.response){

                            append_input_sin_vacacion(response.response[persona].id)
                            $('#id_sin_vacacion' + response.response[persona].id).val(response.response[persona].id)
                            $('#nombre_sin_vacacion' + response.response[persona].id).val(response.response[persona].nombre)
                            $('#b_sin_vacacion' + response.response[persona].id).prop('checked', false)

                        }

                    }


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
        ajax_call_get('portal_vacacion_update', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            $('#id').val(self.id)
            $('#fktipovacacion').val(self.fktipovacacion)
            $('#fktipovacacion').selectpicker('refresh')
            $('#fkpersona').val(self.fkpersona)
            $('#fkpersona').selectpicker('refresh')
            $('#descripcion').val(self.descripcion)
            $('#dias').val(self.dias)
            $('#fechai').val(self.fechai)
            $('#fechaf').val(self.fechaf)

            $('#estadoautorizacion').val(self.estadoautorizacion)
            $('#estadoaprobacion').val(self.estadoaprobacion)

            cambio_tipo_vacacion(parseInt(JSON.parse($('#fktipovacacion').val())))
            obtener_dias_vacacion($('#fkpersona').val())


            color_input()


            $('.module').prop('checked', false)
            $('#personal_div').empty()

            if (parseInt(JSON.parse(self.fktipovacacion)) ==1 || parseInt(JSON.parse(self.fktipovacacion)) ==4){
                $('#div_medio_dia').hide()
                $('#row_colectivo').hide()

                document.getElementById('mañana').checked=false
                document.getElementById('tarde').checked=false

            } else if(parseInt(JSON.parse(self.fktipovacacion)) == 2){
                $('#div_medio_dia').show()
                $('#row_colectivo').hide()

                if (self.jornada == "Mañana"){
                    document.getElementById('mañana').checked=true
                    document.getElementById('tarde').checked=false
                }else if (self.jornada == "Tarde"){
                    document.getElementById('mañana').checked=false
                    document.getElementById('tarde').checked=true
                }

            }else if(parseInt(JSON.parse(self.fktipovacacion)) == 3){
                 $('#div_medio_dia').hide()
                $('#row_colectivo').show()
                document.getElementById('mañana').checked=false
                document.getElementById('tarde').checked=false
                
                for(i in self.colectiva){
                    employe_cb = $('.employee[data-id="'+self.colectiva[i].fkpersona+'"]')
                    employe_cb.prop('checked', true)
                    analizar(employe_cb.parent().parent().closest('.dd-list').prev().find('.module'))
                }
            }





            //clean_form()
            verif_inputs('')
            validationInputSelects("form")
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
        ajax_call_get('portal_vacacion_autorizacion', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            console.log(self)
            $('#id').val(self.id)
            $('#fktipovacacion').val(self.fktipovacacion)
            $('#fktipovacacion').selectpicker('refresh')
            $('#fkpersona').val(self.fkpersona)
            $('#fkpersona').selectpicker('refresh')
            $('#pid').val(self.fkpersona)
            $('#descripcion').val(self.descripcion)
            $('#dias').val(self.dias)
            $('#fechai').val(self.fechai)
            $('#horai').val(self.horai)
            $('#fechaf').val(self.fechaf)
            $('#horaf').val(self.horaf)
            $('#respuestaautorizacion').val(self.respuestaautorizacion)
            $('#respuestaaprobacion').val(self.respuestaaprobacion)

            $('#estadoautorizacion').val(self.estadoautorizacion)
            $('#estadoaprobacion').val(self.estadoaprobacion)

            obtener_dias_vacacion($('#fkpersona').val())

            cambio_tipo_vacacion(parseInt(JSON.parse($('#fktipovacacion').val())))

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
        ajax_call_get('portal_vacacion_aprobacion', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            $('#id').val(self.id)
            $('#fktipovacacion').val(self.fktipovacacion)
            $('#fktipovacacion').selectpicker('refresh')
            $('#fkpersona').val(self.fkpersona)
            $('#fkpersona').selectpicker('refresh')
            $('#pid').val(self.fkpersona)
            $('#descripcion').val(self.descripcion)
            $('#dias').val(self.dias)
            $('#fechai').val(self.fechai)
            $('#horai').val(self.horai)
            $('#fechaf').val(self.fechaf)
            $('#horaf').val(self.horaf)
            $('#respuestaautorizacion').val(self.respuestaautorizacion)
            $('#respuestaaprobacion').val(self.respuestaaprobacion)

            $('#estadoautorizacion').val(self.estadoautorizacion)
            $('#estadoaprobacion').val(self.estadoaprobacion)

            obtener_dias_vacacion($('#fkpersona').val())

            cambio_tipo_vacacion(parseInt(JSON.parse($('#fktipovacacion').val())))

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
            url: '/portal_vacacion_imprimir',
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
    if (notvalid===false) {
        objeto = JSON.stringify({
            'id': parseInt($('#id').val()),
            'fktipovacacion': $('#fktipovacacion').val(),
            'fkpersona': $('#fkpersona').val(),
            'descripcion': $('#descripcion').val(),
            'fechai': $('#fechai').val(),
            'fechaf': $('#fechaf').val(),
            'mañana':document.getElementById('mañana').checked,
            'tarde':document.getElementById('tarde').checked,
            'estado': $('#estado').val()
        })
        ajax_call('portal_vacacion_update', {
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
            'respuestaautorizacion': $('#respuesta').val()
        })
        ajax_call('portal_vacacion_autorizacion', {
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
        ajax_call('portal_vacacion_aprobacion', {
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
        title: "¿Desea dar de baja los datos de la portal_vacacion?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#1565c0",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    }).then(function () {
        ajax_call('portal_vacacion_delete', {
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


function ajax_call_solicitud(url, data, render, callback) {
    $.ajax({
        method: "POST",
        url: url,
        data: data,
        async: false
    }).done(function (response) {

        response = JSON.parse(response)
        exito = response.success;
        response = response.response;
        //si exito es verdarero, se inserto portal_vacacion
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

var inputdias = document.getElementById('dias')
inputdias.onfocusout = function (){ this.parentElement.classList.add('focused')}

var inputfechaf = document.getElementById('fechaf')
inputfechaf.onfocusout = function (){ this.parentElement.classList.add('focused')}

validationKeyup("form");
validationSelectChange("form");