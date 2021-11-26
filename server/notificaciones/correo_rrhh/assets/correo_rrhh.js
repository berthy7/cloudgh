main_route = '/correo_rrhh'

$(document).ready(function () {
    $('#data_table').DataTable();
});

$(document).ajaxStart(function () { });

$(document).ajaxStop(function () {
    $.Toast.hideToast();
});

var id_gv = 0


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

    $('#personal_div').empty()

    verif_inputs('')
    validationInputSelects("form");
    $('#id_div').hide()
    $('#insert').show()
    $('#form').modal('show')

})


$('#insert').click(function () {

    notvalid = validationInputSelectsWithReturn("form");
    if (notvalid===false) {
        objeto = JSON.stringify({
            'correos': obtener_personas()
        })
        ajax_call('correo_rrhh_insert', {
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
            'Ninguna persona agregada.',
             '',
            'warning'
        )
        $('#form').modal('hide')
    }

})

reload_form()

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
        ajax_call("correo_rrhh_delete", objeto)
    })
})

validationKeyup("form")
validationSelectChange("form")