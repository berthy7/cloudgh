main_route = '/asistenciapersonal'

$(document).ready(function () { });

$(document).ajaxStart(function () { });

$(document).ajaxStop(function () {
    $.Toast.hideToast();
});

var fechahoy = new Date()
var hoy = fechahoy.getDate()+"/"+(fechahoy.getMonth()+1) +"/"+fechahoy.getFullYear()

document.getElementById("fechainicio").value=hoy
document.getElementById("fechafin").value=hoy


$('.show-tick').selectpicker()
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

            return {
                'id_persona': a
            }


        })(a))
    })
    return aux
}

function obtener_personas() {
        objeto = []
        objeto_inputs = $('.personal')

        for (i = 0; i < objeto_inputs.length; i += 1) {
            h0 = objeto_inputs[i].value


            objeto.push((function add_objeto(h0) {

                    return {
                    'id_persona':h0
                    }


            })(
                objeto_inputs[i].value))
        }
        return objeto
    }


function cargar_tabla(data){
    if ( $.fn.DataTable.isDataTable( '#data_table' ) ) {
        var table = $('#data_table').DataTable();
        table.destroy();
    }

    $('#data_table').DataTable({
        data:           data,
        deferRender:    true,
        scrollCollapse: true,
        scroller:       true,

        dom: "Bfrtip" ,
        buttons: [
            {  extend : 'excelHtml5',
               exportOptions : { columns : [0, 1, 2, 3, 4, 5 ,6 ,7 ,8 ,9 ,10]},
                sheetName: 'Reporte de Asistencia',
               title: 'ELFEC - Reporte de Asistencia'  },
            {  extend : 'pdfHtml5',
                orientation: 'landscape',
               customize: function(doc) {
                    doc.styles.tableBodyEven.alignment = 'center';
                    doc.styles.tableBodyOdd.alignment = 'center';
               },
               exportOptions : {
                    columns : [0, 1, 2, 3, 4, 5 ,6 ,7 ,8 ,9 ,10]
                },
               title: 'ELFEC - Reporte de Asistencia'
            }
        ],
        initComplete: function () {
            $("#rgm-loader").fadeOut('800');
            document.getElementById("filtrar").disabled = false
        },
        "order": [[ 1, "desc" ]],
        language : {
            'url': '/resources/js/spanish.json',
        },
        "pageLength": 50
    });
}


$('#new').click(function () {
    obj = JSON.stringify({
        'fechainicio': $('#fechainicio').val(),
        'fechafin': $('#fechafin').val(),
        '_xsrf': getCookie("_xsrf")
    })
    ruta = 'asistenciapersonal_insert';

    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: true,
        beforeSend: function () {
           $("#rproc-loader").fadeIn(800);
           $("#new").hide();
        },
        success: function () {
           $("#rproc-loader").fadeOut(800);
           $("#new").show();
        }
    }).done(function (response) {
        response=JSON.parse(response)
        showMessage("Actualizados correctamente", "success", "ok")

        var data = [];
        for (var i = 0; i < Object.keys(response.response).length; i++) {
            data.push( [
                response['response'][i]["id"],response['response'][i]["codigo"],response['response'][i]["nombrecompleto"],
                    response['response'][i]["fecha"],response['response'][i]["entrada"],
                    response['response'][i]["salida"],response['response'][i]["mentrada"],
                    response['response'][i]["msalida"],response['response'][i]['observacion'],
                    response['response'][i]["retraso"],response['response'][i]['extra']
            ]);
        }
        console.log("data1:", data )
        cargar_tabla(data)

    })
});

$('#actualizar_marcaciones').click(function () {
    obj = JSON.stringify({
        'fechainicio': $('#fechainicio').val(),
        'fechafin': $('#fechafin').val(),
        '_xsrf': getCookie("_xsrf")
    })
    ruta = 'asistenciapersonal_actualizar_marcaciones';

    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: true,
        beforeSend: function () {
           $("#rproc-loader-marcas").fadeIn(800);
           $("#new").hide();
        },
        success: function () {
           $("#rproc-loader-marcas").fadeOut(800);
           $("#new").show();
        }
    }).done(function (response) {
        response=JSON.parse(response)
        showMessage("Actualizado correctamente", "success", "ok")

        var data = [];
        for (var i = 0; i < Object.keys(response.response).length; i++) {
            data.push( [
                response['response'][i].id,response['response'][i].codigo,response['response'][i].nombrecompleto,
                response['response'][i].fecha,response['response'][i].entrada,
                response['response'][i].salida,response['response'][i].mentrada,
                response['response'][i].msalida,response['response'][i].observacion,
                response['response'][i].retraso,response['response'][i].extra
            ]);
        }

        cargar_tabla(data)

    })
});

$('#filtrar').click(function () {
    $("#rgm-loader").show();
    document.getElementById("filtrar").disabled = true
    obj = JSON.stringify({
        'fechainicio': $('#fechainicio').val(),
        'fechafin': $('#fechafin').val(),
        '_xsrf': getCookie("_xsrf")
    })
    ruta = "asistenciapersonal_filtrar";
    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: true
    }).done(function (response) {
        response = JSON.parse(response)

        var data = [];
        for (var i = 0; i < Object.keys(response.response).length; i++) {

            data.push( [
                response['response'][i]["id"],response['response'][i]["codigo"],response['response'][i]["nombre"],
                response['response'][i]["fecha"],response['response'][i]["entrada"],
                response['response'][i]["salida"],response['response'][i]["mentrada"],
                response['response'][i]["msalida"],response['response'][i]['observacion'],
                response['response'][i]["retraso"],response['response'][i]['extra']
            ]);
        }

        cargar_tabla(data)
    })
});


$('#insert').click(function () {
    values = "nombre";
    if (validate_inputs_empty(values)) {
        objeto = JSON.stringify({
            'nombre': $('#nombre').val()
        })

        ajax_call('asistenciapersonal_insert', {
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

$('#boleta').click(function () {
    $('#fechainicioboleta').val($('#fechainicio').val())
    $('#fechafinboleta').val($('#fechafin').val())
    $('#personal_div').empty()
    $('#form-boleta').modal('show')
})


function attach_edit() {
    $('.edit').click(function () {
        obj = JSON.stringify({
            'id': parseInt(JSON.parse($(this).attr('data-json')))
        })

        ajax_call_get('asistenciapersonal_update', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            $('#id').val(self.id)
            $('#nombre').val(self.nombre)

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
    if (!validationInputSelects("form")) {
        objeto = JSON.stringify({
            'id': parseInt($('#id').val()),
            'nombre': $('#nombre').val()
        })
        ajax_call('asistenciapersonal_update', {
            object: objeto,
            _xsrf: getCookie("_xsrf")
        }, null, function () {
            setTimeout(function () {
                window.location = main_route
            }, 2000);
        })
        $('#form').modal('hide')
    } else {
        swal('Error de datos.',
            'Hay campos vacíos por favor verifique sus datos.',
            'error')
    }
})
reload_form()


$('.delete').click(function () {
    id = parseInt(JSON.parse($(this).attr('data-json')))
    enabled = false

    swal({
        title: "¿Desea dar de baja la asistencia personal?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#1565c0",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    }).then(function () {
        ajax_call('asistenciapersonal_delete', {
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

 $('#generar_pdf').click(function () {
    obj = JSON.stringify({
        'fechainicio': $('#fechainicioboleta').val(),
        'fechafin': $('#fechafinboleta').val(),
        'personas_arbol': obtener_personas_arbol(),
        'personas': obtener_personas(),
        '_xsrf': getCookie("_xsrf")
    })

    $.ajax({
        method: "POST",
        url: '/asistenciapersonal_boleta_pdf',
        data: {object: obj, _xsrf: getCookie("_xsrf")}
    }).done(function(response){
        dictionary = JSON.parse(response)
        dictionary = dictionary.response
        servidor = ((location.href.split('/'))[0])+'//'+(location.href.split('/'))[2];
        url = servidor + dictionary;

        window.open(url)
    })
})

$('#reporte-xls').click(function () {
    aux = {'datos': table_pdf}
    obj = JSON.stringify(aux)
    ruta = "/analisis_reporte_xls";
    $.ajax({
        method: "POST",
        url: ruta,
        data:{_xsrf: getCookie("_xsrf"), object: obj},
        async: false
    }).done(function(response){
        response = JSON.parse(response)

        if (response.success) {
            $('#link_excel').attr('href', response.response.url).html(response.response.nombre)
        }
    })
    $('#modal-rep-xls').modal('show')
})