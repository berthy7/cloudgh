main_route = '/permiso'

$(document).ready(function () { });

$(document).ajaxStart(function () { });

$(document).ajaxStop(function () {
    $.Toast.hideToast();
});

$('#data_table').DataTable({

        dom: "Bfrtip" ,
        buttons: [
            {  extend : 'excelHtml5',
               exportOptions : { columns : [0, 1, 2, 3, 4, 5 ,6 ,7,8]},
                sheetName: 'Autorizacion de salida',
               title: 'Autorizacion de salida'  },
            {  extend : 'pdfHtml5',
                orientation: 'landscape',
               customize: function(doc) {
                    doc.styles.tableBodyEven.alignment = 'center';
                    doc.styles.tableBodyOdd.alignment = 'center';
               },
               exportOptions : {
                    columns : [0, 1, 2, 3, 4, 5 ,6 ,7,8]
                },
               title: 'Autorizacion de salida'
            }
        ],
        "order": [[ 0, "desc" ]],
        language : {
            'url': '/resources/js/spanish.json',
        },
        "pageLength": 50
    });

var fechahoy = new Date();
var hoy = fechahoy.getDate()+"/"+(fechahoy.getMonth()+1) +"/"+fechahoy.getFullYear()
$(".hr").inputmask("h:s",{ "placeholder": "__/__" });

document.getElementById("fechai").value=hoy
document.getElementById("fechaf").value=hoy

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

$('#fktipoausencia').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
})

$('#fkpersona').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar persona',
    title: 'Seleccione una persona'
})

$('#fktipoausencia').change(function () {
    cargar_tipoausencia($('#fktipoausencia').val(),"nuevo")
});

function cargar_tipoausencia(idausencia,tipo) {
    obj = JSON.stringify({
        'tipoausencia': idausencia,
        '_xsrf': getCookie("_xsrf")
    })

    ruta = "tipoausencia_obtener";
    //data.append('object', obj)
    //data.append('_xsrf',getCookie("_xsrf"))

    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: false
    }).done(function (response) {
        response = JSON.parse(response)

        //console.log(response)
        $('#disponibilidad').val(response.response.disponibilidad + " " + response.response.selec_disponibilidad)
        $('#dia').val(response.response.disponibilidad)
        $('#dia_disponibilidad').val(response.response.selec_disponibilidad)
        $('#duracion').val(response.response.duracion + " " + response.response.selec_duracion)
        $('#tiempo').val(response.response.duracion)
        $('#tiempo_duracion').val(response.response.selec_duracion)

        if (tipo === "nuevo"){
            $('#div_fechaf').hide()
            $('#div_horaf').hide()
            $('#dtfin').parent().hide()

            if (response.response.selec_duracion === "Dia"){
                $('#div_horai').hide()
                $('#div_horaf').hide()
            }
            else if (response.response.selec_duracion === "1/2 Dia"){
                $('#div_horai').show()
                $('#div_horaf').hide()
            }
            else if (response.response.selec_duracion === "Ilimitado"){
                $('#div_fechaf').show()
                $('#dtfin').parent().show()
                $('#div_horai').show()
                $('#div_horaf').show()
            }
            else $('#div_horai').show();
        }
    })
}

$('#new').click(function () {
    $('#fktipoausencia').val('')
    $('#fktipoausencia').selectpicker('refresh')
    $('#fkpersona').val('')
    $('#fkpersona').selectpicker('refresh')
    $('#descripcion').val('')
    document.getElementById("fechai").value=hoy
    $('#fechaf').val('')
    $('#disponibilidad').val('')
    $('#duracion').val('')

    // document.getElementById("fechaf").value=hoy
    $('#dtini').calendar('setDate', str_to_date($('#fechai').val()))
    $('#dtfin').calendar('setDate', str_to_date($('#fechai').val()))

    $('#estadoautorizacion').val('Pendiente')
    $('#estadoaprobacion').val('Pendiente')

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
    if (notvalid===false) {
        objeto = JSON.stringify({
            'fktipoausencia': $('#fktipoausencia').val(),
            'fkpersona': $('#fkpersona').val(),
            'descripcion': $('#descripcion').val(),
            'fechai': $('#fechai').val(),
            'horai': $('#horai').val(),
            'fechaf': $('#fechaf').val(),
            'horaf': $('#horaf').val(),
            'tiempo': $('#tiempo').val(),
            'tiempo_duracion': $('#tiempo_duracion').val()
        })

        if($('#dia_disponibilidad').val() == "Ilimitado"){
            ajax_call('permiso_insert', {
                object: objeto,
                _xsrf: getCookie("_xsrf")
            }, null, function () {
                setTimeout(function () {
                    window.location = main_route
                }, 2000);
            })

            $('#form').modal('hide')
        }else{

            objeto_verificar = JSON.stringify({
                'fkpersona': $('#fkpersona').val(),
                'fktipoausencia': $('#fktipoausencia').val(),
                'dia': $('#dia').val(),
                'fechai': $('#fechai').val()

            })

            ajax_call_post("permiso_disponible", {
                _xsrf: getCookie("_xsrf"),
                object: objeto_verificar
                }, function (response) {
                    if(response.success === true){

                        ajax_call('permiso_insert', {
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
        }
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
        $('#dtini').calendar('clear')
        $('#dtfin').calendar('clear')

        obj = JSON.stringify({
            'id': parseInt(JSON.parse($(this).attr('data-json')))
        })

        ajax_call_get('permiso_update', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            $('#id').val(self.id)
            $('#fkpersona').val(self.fkpersona)
            $('#fkpersona').selectpicker('refresh')
            $('#fktipoausencia').val(self.fktipoausencia)
            $('#fktipoausencia').selectpicker('refresh')
            $('#descripcion').val(self.descripcion)
            
            $('#fechai').val(self.fechai)
            $('#fechaf').val(self.fechaf)
            $('#horai').val(self.horai)
            $('#horaf').val(self.horaf)

            if (![null, '', 'None'].includes(self.fechai)) $('#dtini').calendar('setDate', str_to_date($('#fechai').val()))
            if (![null, '', 'None'].includes(self.fechaf)) $('#dtfin').calendar('setDate', str_to_date($('#fechaf').val()))
            
            $('#estadoautorizacion').val(self.estadoautorizacion)
            $('#estadoaprobacion').val(self.estadoaprobacion)
            cargar_tipoausencia($('#fktipoausencia').val(),"")

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
        ajax_call_get('permiso_autorizacion', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            console.log(self)
            $('#id').val(self.id)
            $('#fktipoausencia').val(self.fktipoausencia)
            $('#fktipoausencia').selectpicker('refresh')
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

            cargar_tipoausencia($('#fktipoausencia').val(),"")

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
        ajax_call_get('permiso_aprobacion', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            $('#id').val(self.id)
            $('#fktipoausencia').val(self.fktipoausencia)
            $('#fktipoausencia').selectpicker('refresh')
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

            cargar_tipoausencia($('#fktipoausencia').val(),"")

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
            url: '/permiso_imprimir',
            data: {object: obj, _xsrf: getCookie("_xsrf")}
        }).done(function (response) {
            dictionary = JSON.parse(response)
            dictionary = dictionary.response
            servidor = ((location.href.split('/'))[0]) + '//' + (location.href.split('/'))[2];
            url = servidor + dictionary;

            window.open(url)
        })
    })
    
    $('#imprimir_general').click(function () {
        obj = JSON.stringify({
            'id': ''
        })
        $.ajax({
            method: "POST",
            url: '/permiso_imprimir_general',
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
            'nombre': $('#nombre').val(),
            'descripcion': $('#descripcion').val()
        })
        ajax_call('permiso_update', {
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
        ajax_call('permiso_autorizacion', {
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
        ajax_call('permiso_aprobacion', {
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
//             ajax_call('permiso_delete', {
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
        cb_title = "¿Está seguro de que desea dar de baja la autorizacion de salida?"

    } else {
        cb_title = "¿Está seguro de que desea dar de alta la autorizacion de salida?"
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
        ajax_call('permiso_delete', {
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

var inputHoraInicio = document.getElementById('horai') ,
    inputHoraFin = document.getElementById('horaf')
inputHoraInicio.onfocusout = function (){ this.parentElement.classList.add('focused')}
inputHoraFin.onfocusout = function (){ this.parentElement.classList.add('focused')}

validationKeyup("form");
validationSelectChange("form");
