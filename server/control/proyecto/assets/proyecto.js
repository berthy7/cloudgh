main_route = '/proyecto'

i_task= 0;
del_rev = [];
isvalid = 0;

$(document).ready(function () {
    var tabledt = $('#data_table').DataTable();
    tabledt.order([1, 'asc']).draw();
    sliderBasic.setAttribute('disabled', true);
});

$(document).ajaxStart(function () { });

$(document).ajaxStop(function () {
    $.Toast.hideToast();
});

function getNoUISliderValue(slider, percentage) {
    slider.noUiSlider.on('update', function () {
        var val = slider.noUiSlider.get();
        if (percentage) {
            val = parseInt(val);
            val += '%';
        }
        $(slider).parent().find('span.js-nouislider-value').text(val);
    });
}

var sliderBasic = document.getElementById('nouislider_basic_example');
noUiSlider.create(sliderBasic, {
    start: [0],
    connect: 'lower',
    step: 1,
    range: {
        'min': [0],
        'max': [100]
    }
});
getNoUISliderValue(sliderBasic, true);



function attach_edit() {
    $('.edit').click(function () {
        del_task = [];
        var table = $('#table_tasks').DataTable();
        table.clear().draw();

        obj = JSON.stringify({
            'id': parseInt(JSON.parse($(this).attr('data-json')))
        })
        ajax_call_get('proyecto_update', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            console.log(self)
            $('#id').val(self.id)
            var tareas_terminadas = 0

            $('#nombre').val(self.nombre)
            $('#descripcion').val(self.descripcion)

            for(var i = 0; i < self.tareas.length; i++){
                console.log(self.tareas[i].enabled)
                if(self.tareas[i].enabled){
                    var datos_field  = [self.tareas[i].id, self.tareas[i].fkpersona, self.tareas[i].descripcion, self.tareas[i].prioridad, self.tareas[i].estimacion,
                                        self.tareas[i].fechaInicio, self.tareas[i].fechaFin, self.tareas[i].estado];
                    append_field_task(datos_field );
                    if(self.tareas[i].estado =="Terminado"){
                        tareas_terminadas = tareas_terminadas + 1;
                    }
                }
            }

            var tareas = self.tareas.length;
            var porcentaje = tareas_terminadas / tareas * 100

            sliderBasic.noUiSlider.set(porcentaje);

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

    for(i=0; i<objeto_inputs.length; i+=11){
        h0 = objeto_inputs[i].value
        h1 = objeto_inputs[i+1].value
        h2 = objeto_inputs[i+3].value
        h3 = objeto_inputs[i+5].value
        h4 = objeto_inputs[i+6].value
        h5 = objeto_inputs[i+7].value
        h6 = objeto_inputs[i+8].value
        h7 = objeto_inputs[i+10].value


        if (h2 === '' ) {
            h2 = null
            console.log("valor: ",h2)
        }
        if (h3 === '' ) {
            h3 = null
            console.log("valor: ",h3)
        }
        if (h4 === '' ) {
            h4 = null
            console.log("valor: ",h4)
        }
        if (h5 === '' ) {
            h5 = null
            console.log("valor: ",h5)
        }
        if (h6 === '' ) {
            h6 = null
            console.log("valor: ",h6)
        }
        if (h7 === '' ) {
            h7 = null
            console.log("valor: ",h7)
        }

        if(h0 === '' || h1 === ''){
            console.log("sin datos")
        }else{

            objeto.push((function add_objeto(h0, h1, h2, h3, h4, h5, h6, h7) {


                if (h0 == '0'){
                    return {

                        'descripcion': h1,
                        'fkpersona':h2,
                        'prioridad': h3,
                        'estimacion': h4,
                        'fechaInicio': h5,
                        'fechaFin': h6,
                        'estado': h7
                    }

                }else{
                    return {
                        'id':h0,
                        'descripcion': h1,
                        'fkpersona':h2,
                        'prioridad': h3,
                        'estimacion': h4,
                        'fechaInicio': h5,
                        'fechaFin': h6,
                        'estado': h7
                    }
                }
            })(
                h0,
                h1,
                h2,
                h3,
                h4,
                h5,
                h6,
                h7
            ))
                }
    }
    return objeto
}


$('#update').click(function () {
    objeto = JSON.stringify({
        'id': parseInt($('#id').val()),
        'nombre': $('#nombre').val(),
        'descripcion': $('#descripcion').val(),
        'tareas': get_tasks(),
        'remove_task': del_task
    })
    if (isvalid === 0){
        swal(
            'Error de datos',
            'Debe ingresar todos los datos requeridos.',
            'warning'
        )
    }else{
        ajax_call('proyecto_update', {
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


$('#new').click(function () {
    del_task = [];
    $('#id').val('')
    $('#nombre').val('')
    $('#descripcion').val('')
    var table = $('#table_tasks').DataTable();
    table.clear().draw();

    verif_inputs('')
    $('#id_div').hide()
    $('#insert').show()
    $('#update').hide()

    $('#form').modal('show')
})

$('#insert').click(function () {
    objeto = JSON.stringify({
        'id': parseInt($('#id').val()),
        'nombre': $('#nombre').val(),
        'descripcion': $('#descripcion').val(),
        'tareas': get_tasks(),
        'remove_task': del_task
    })
    if (isvalid === 0){
        swal(
            'Error de datos',
            'Debe ingresar todos los datos requeridos.',
            'warning'
        )
    }else{
        ajax_call('proyecto_insert', {
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
    ruta = 'proyecto_create';
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
                    'proyectos Creados.',
                    'success'
                )
                $('#form-seg').modal('hide')
            } else {
                swal(
                    'Error.',
                    'proyectos no creados.',
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


$('.show-tick').selectpicker()

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
    ruta = "proyecto_filtrar";
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