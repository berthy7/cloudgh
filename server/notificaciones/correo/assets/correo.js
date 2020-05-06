main_route = '/correo'

$(document).ready(function () {
    $('#data_table').DataTable();
});

$(document).ajaxStart(function () { });

$(document).ajaxStop(function () {
    $.Toast.hideToast();
});

var id_gv = 0
$(".hr").inputmask("h:s",{ "placeholder": "__/__" });

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

        var id_correos = ''
        $("input.correos").each(function() {
            id_correos = $(this).prop('id');
        });

        var id_fkpersona= ''
        $("input.fkpersona").each(function() {
            id_fkpersona = $(this).prop('id');
        });


        $('#' + id_nombres ).val(response.response.fullname)
        $('#' + id_nombres ).parent().addClass('focused')
        $('#' + id_fkpersona ).val(response.response.id)
        $('#' + id_fkpersona ).parent().addClass('focused')
        $('#' + id_correos ).val(response.response.empleado[0].email)
        $('#' + id_correos ).parent().addClass('focused')


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
            <div class="col-md-1 hidden">\
                <div class="input-group">\
                <input  id="fkpersona'+id_in+'" class="form-control fkpersona personal readonly">\
                </div>\
            </div>\
            <div class="col-md-4 p-t-own">\
                <div class="form-group form-float">\
                    <div id="nombresDIV" class="form-line">\
                        <input id="nombres'+id_in+'" data-id="'+id_in+'" class="form-control nombres " readonly>\
                        <label class="form-label">Nombre Completo</label>\
                    </div>\
                </div>\
            </div>\
            <div class="col-md-4 p-t-own">\
                <div class="form-group form-float">\
                    <div id="correosDIV" class="form-line">\
                        <input id="correos'+id_in+'" data-id="'+id_in+'" class="form-control correos" readonly>\
                        <label class="form-label">Correo Electronico</label>\
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

    $('.fkpersona').click(function () {
        $(this).parent().addClass('focused');
        current_input = $(this).prop('id');
    })

}

function obtener_personas() {
        objeto = []
        objeto_inputs = $('.personal')

        for (i = 0; i < objeto_inputs.length; i += 2) {
            h0 = objeto_inputs[i].value
            h1 = objeto_inputs[i+1].value


            objeto.push((function add_objeto(h0,h1) {

                if (h0 == ''){
                    return {
                        'fkpersona':h1
                    }

                }else{
                    return {
                        'id':h0,
                        'fkpersona':h1
                    }
                }


            })(
                objeto_inputs[i].value,
                objeto_inputs[i+1].value))
        }
        return objeto
    }



$('#new').click(function () {

    ajax_call_get('correo_insert', {
        _xsrf: getCookie("_xsrf")
    }, function (response) {
        var self = response;
        $('#id_correos').val(self.id)
        $('#personal_div').empty()

        for (i in self.correos) {

            append_input_personal('')
            var id_nombres = ''
            $("input.nombres").each(function() {
                id_nombres  = $(this).prop('id');
            });
            var id_id = ''
            $("input.idnombres").each(function() {
                id_id = $(this).prop('id');
            });

            var id_fkpersona= ''
            $("input.fkpersona").each(function() {
                id_fkpersona = $(this).prop('id');
            });

            var id_correos = ''
            $("input.correos").each(function() {
                id_correos = $(this).prop('id');
            });

            $('#' + id_id ).val(self.correos[i].id)
            $('#' + id_id ).parent().addClass('focused')
            $('#' + id_fkpersona ).val(self.correos[i].fkpersona)
            $('#' + id_fkpersona ).parent().addClass('focused')
            $('#' + id_nombres ).val(self.correos[i].persona.fullname)
            $('#' + id_nombres ).parent().addClass('focused')
            $('#' + id_correos ).val(self.correos[i].persona.empleado[0].email)
            $('#' + id_correos ).parent().addClass('focused')

        }
        verif_inputs('')
        validationInputSelects("form");
        $('#id_div_correos').hide()
        $('#insert').show()
        $('#form_correos').modal('show')
    })


})


$('#insert').click(function () {
    var sw = obtener_personas()

    if (sw.length !== 0) {
        objeto = JSON.stringify({
            'id': parseInt($('#id_correos').val()),
            'correos': obtener_personas()
        })
        ajax_call('correo_insert', {
            object: objeto,
                _xsrf: getCookie("_xsrf")
            }, null, function () {
                setTimeout(function () {
                window.location = main_route
            }, 2000);
        })
        $('#form_correos').modal('hide')
    } else {
        swal(
            'Ninguna persona agregada.',
             '',
            'warning'
        )
        $('#form_correos').modal('hide')
    }

})


function attach_edit() {
    $('#edit').click(function () {
        obj = JSON.stringify({
            'id': 1
        })
        ajax_call_get('correo_update', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            $('#id').val(self.id)
            $('#servidor').val(self.servidor)
            $('#puerto').val(self.puerto)
            $('#correo').val(self.correo)
            $('#password').val(self.password)

            clean_form()
            verif_inputs('')
            $('#id_div').hide()
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
            'servidor': $('#servidor').val(),
            'puerto': $('#puerto').val(),
            'correo': $('#correo').val(),
            'password': $('#password').val()
        })
        ajax_call('correo_update', {
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

$('#edit_hora').click(function () {

        objeto = JSON.stringify({
            'hora': $('#hora_correo').val()
        })
        ajax_call('correo_hora', {
            object: objeto,
            _xsrf: getCookie("_xsrf")
        }, null, function () {
            setTimeout(function () {
                window.location = main_route
            }, 2000);
        })

})
reload_form()


$('.delete').click(function () {
    id = parseInt(JSON.parse($(this).attr('data-json')))
    enabled = false
    swal({
        title: "¿Desea dar de baja los datos de la correo?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#1565c0",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    }).then(function () {
        ajax_call('correo_delete', {
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

$('.enabled_dias').click(function (e) {
    e.preventDefault()
    cb_delete = this
    b=$(this).prop('checked')//$(this).is('checked')
    if(!b){
        cb_title = "¿Está seguro de que desea dar de baja el dia ?"
    } else {
        cb_title ="¿Está seguro de que desea dar de alta el dia?"
    }
    swal({
        text: cb_title,
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#673AB7",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    }).then(function () {
        $(cb_delete).prop('checked', !$(cb_delete).is(':checked'))
        objeto = {
            id: parseInt($(cb_delete).attr('data-id')),
            enabled: $(cb_delete).is(':checked'),
            _xsrf: getCookie("_xsrf")
        }
        ajax_call("correo_dias", objeto)
    })
})

$('.enabled').click(function (e) {
    e.preventDefault()
    cb_delete = this
    b=$(this).prop('checked')//$(this).is('checked')
    if(!b){
        cb_title = "¿Está seguro de que desea dar de baja el correo ?"
    } else {
        cb_title ="¿Está seguro de que desea dar de alta el correo?"
    }
    swal({
        text: cb_title,
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#673AB7",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    }).then(function () {
        $(cb_delete).prop('checked', !$(cb_delete).is(':checked'))
        objeto = {
            id: parseInt($(cb_delete).attr('data-id')),
            enabled: $(cb_delete).is(':checked'),
            _xsrf: getCookie("_xsrf")
        }
        ajax_call("correo_delete", objeto)
    })
})

validationKeyup("form")
validationSelectChange("form")