main_route = '/tarea'

i_task= 0;
del_rev = [];
isvalid = 0;

$(document).ready(function () {
    var tabledt = $('#data_table').DataTable();
    tabledt.order([1, 'asc']).draw();
});

$(document).ajaxStart(function () { });

$(document).ajaxStop(function () {
    $.Toast.hideToast();
});


function attach_edit() {
    $('.edit').click(function () {
        del_task = [];
        var table = $('#table_tasks').DataTable();
        table.clear().draw();

        obj = JSON.stringify({
            'id': parseInt(JSON.parse($(this).attr('data-json')))
        })
        ajax_call_get('tarea_update', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            console.log(self)

            $('#idseg').val(self[0].persona.id)
            $('#rdpersona').val(self[0].persona.fullname)

            for(var i = 0; i < self.length; i++){
                console.log(self[i].enabled)
                if(self[i].enabled){
                    var datos_field  = [self[i].id, self[i].fkproyecto, self[i].descripcion, self[i].prioridad, self[i].estimacion,
                                        self[i].fechaInicio, self[i].fechaFin, self[i].estado];
                    append_field_task(datos_field );
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


function get_tasks() {
    isvalid = 1;
    objeto = [];
    objeto_inputs = $('.tasks')
    console.log(objeto_inputs)
    if(objeto_inputs.length === 0) isvalid = 0;

    for(i=0; i<objeto_inputs.length; i+=11){
        h0 = objeto_inputs[i].value
        h1 = objeto_inputs[i+2].value
        h2 = objeto_inputs[i+3].value
        h3 = objeto_inputs[i+5].value
        h4 = objeto_inputs[i+6].value
        h5 = objeto_inputs[i+7].value
        h6 = objeto_inputs[i+8].value
        h7 = objeto_inputs[i+10].value
        if(h0 === '' || h1 === '' ||h2 === '' ||h3 === '' ||h4 === '' ||h5 === '' ||h6 === '' || h7 === '') isvalid = 0;

        objeto.push((function add_objeto(h0, h1, h2, h3, h4, h5, h6, h7) {
            return {
                'id':h0,
                'fkproyecto':h1,
                'descripcion': h2,
                'prioridad': h3,
                'estimacion': h4,
                'fechaInicio': h5,
                'fechaFin': h6,
                'estado': h7
            }
        })(
            objeto_inputs[i].value,
            objeto_inputs[i+2].value,
            objeto_inputs[i+3].value,
            objeto_inputs[i+5].value,
            objeto_inputs[i+6].value,
            objeto_inputs[i+7].value,
            objeto_inputs[i+8].value,
            objeto_inputs[i+10].value
        ))
    }
    return objeto
}


$('#save-tasks').click(function () {
    objeto = JSON.stringify({
        'id': parseInt($('#idseg').val()),
        'datos': get_tasks(),
        'remove_task': del_task
    })
    console.log(objeto)
    if (isvalid === 0){
        swal(
            'Error de datos',
            'Debe ingresar todos los datos requeridos.',
            'warning'
        )
    }else{
        ajax_call('tarea_insert', {
            object: objeto,
                _xsrf: getCookie("_xsrf")
            }, null, function () {
                setTimeout(function () {
                window.location = main_route
            }, 2000);
        })
        $('#form').modal('hide')
    }
})


$('#new-seg').click(function () {
    obj = JSON.stringify({
        '_xsrf': getCookie("_xsrf")
    })
    ruta = 'asistenciapersonal_insertseg';

    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: true,
        beforeSend: function () {
           $("#rproc-loader").fadeIn(800);
           $("#new-seg").hide();
        },
        success: function () {
           $("#rproc-loader").fadeOut(800);
           $("#new-seg").show();
        }
    }).done(function (response) {
        valor=JSON.parse(response)
        if(valor.success) {
            swal(
                'Correcto.',
                'tareas creados.',
                'success'
            )
        } else {
            swal(
                'Error.',
                'tareas no creados.',
                'error'
            )
        }
    })
});

$('#fechaini').bootstrapMaterialDatePicker({
    format: 'YYYY-MM-DD',
    clearButton: false,
    weekStart: 1,
    locale: 'es',
    time: false
}).on('change', function (e, date) {
    $(this).parent().addClass('focused');
});

$('#fechafin').bootstrapMaterialDatePicker({
    format: 'YYYY-MM-DD',
    clearButton: false,
    weekStart: 1,
    locale: 'es',
    time: false
}).on('change', function (e, date) {
    $(this).parent().addClass('focused');
    fecha = document.getElementById("fechaini").value
    $('#fechafin').bootstrapMaterialDatePicker('setMinDate', fecha);
});

$('#fkpersona').selectpicker({
    size: 7,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar persona',
    title: 'Seleccione persona.'
})


$('#add-seg').click(function () {
    $('#fechaini').val('')
    $('#fechafin').val('')
    $('#fkpersona').val('')
    $('#fkpersona').selectpicker('render')

    $('#form-seg').modal('show')
})


$('#save-seg').click(function () {
    obj = JSON.stringify({
        'fkpersona': $('#fkpersona').val(),
        'fechaini': $('#fechaini').val(),
        'fechafin': $('#fechafin').val(),
        '_xsrf': getCookie("_xsrf")
    })
    ruta = 'tarea_create';
    if($('#fkpersona').val() !== '' && $('#fechaini').val() !== '' && $('#fechafin').val() !== ''){
        $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: true,
        beforeSend: function () {
           $("#spn-addsg").fadeIn(800);
           $("#save-seg").hide();
        },
        success: function () {
           $("#spn-addsg").fadeOut(800);
           $("#save-seg").show();
        }
    }).done(function (response) {
            valor = JSON.parse(response)

            if(valor.success) {
                swal(
                    'Correcto.',
                    'tareas Creados.',
                    'success'
                )
                $('#form-seg').modal('hide')
            } else {
                swal(
                    'Error.',
                    'tareas no creados.',
                    'error'
                )
            }
        })
    }else{
        swal(
            'Error.',
            'Ingrese todos los datos requeridos.',
            'warning'
        )
    }

});


var datetoday = new Date()
var today = datetoday.getFullYear() + "-" + (datetoday.getMonth() + 1) + "-" + datetoday.getDate();

document.getElementById("dateinit").value = today
$('.show-tick').selectpicker()


document.getElementById("datelast").value = today
$('.date').bootstrapMaterialDatePicker({
    format: 'YYYY-MM-DD',
    clearButton: false,
    weekStart: 1,
    locale: 'es',
    time: false
}).on('change', function (e, date) {
    $(this).parent().addClass('focused');
    eraseError(this)
});
$('.datepicker').bootstrapMaterialDatePicker({
    format: 'YYYY-MM-DD',
    clearButton: false,
    weekStart: 1,
    locale: 'es',
    time: false
}).on('change', function (e, date) {
    $(this).parent().addClass('focused');
    $('#datelast').bootstrapMaterialDatePicker('setMinDate', date);
});


/*
$('#filtrar').click(function () {
    $("#filter-loader").show();
    document.getElementById("filtrar").disabled = true
    obj = JSON.stringify({
        'fechainicio': $('#dateinit').val(),
        'fechafin': $('#datelast').val(),
        '_xsrf': getCookie("_xsrf")
    })
    ruta = "tarea_filtrar";
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
                response['response'][i]["msalida"],response['response'][i]['observacion']
            ]);
        }

        var table = $('#data_table').DataTable();
        table.destroy();

        $('#data_table').DataTable({
            data:           data,
            deferRender:    true,
            scrollCollapse: true,
            scroller:       true,

            dom: "Bfrtip" ,
            buttons: [
                {  extend : 'excelHtml5',
                   exportOptions : { columns : [0, 1, 2, 3, 4, 5]},
                    sheetName: 'Marcaciones Registradas',
                   title: 'ELFEC - Marcaciones Registradas'  },
                {  extend : 'pdfHtml5',
                   customize: function(doc) {
                        doc.styles.tableBodyEven.alignment = 'center';
                        doc.styles.tableBodyOdd.alignment = 'center';
                   },
                   exportOptions : {
                        columns : [0, 1, 2, 3, 4, 5]
                    },
                   title: 'ELFEC - Marcaciones Registradas'
                }
            ],
            initComplete: function () {
                $("#filter-loader").fadeOut('800');
                document.getElementById("filtrar").disabled = false
            },
            "order": [[ 1, "desc" ]],
            language : {
                'url': '/resources/js/spanish.json',
            },
            "pageLength": 50
        });
    })
});*/