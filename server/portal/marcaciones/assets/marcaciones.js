main_route = '/portal_marcaciones'

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
    format: 'D/MM/YYYY',
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
    $('#ip').val('')
    $('#puerto').val('')
    $('#descripcion').val('')
    $('#email').val('')
    $('#tipo').val("A")
    $('#fksucursal').val('')


    verif_inputs('')
    $('#id_div').hide()
    $('#insert').show()
    $('#update').hide()
    $('#form').modal('show')
})


$('#insert').click(function () {
    values = "ip";
    if (validate_inputs_empty(values)) {
        objeto = JSON.stringify({
            'ip': $('#ip').val(),
            'puerto': $('#puerto').val(),
            'descripcion': $('#descripcion').val(),
            'email': $('#email').val(),
            'tipo': $('#tipo').val(),
            'fksucursal': $('#fksucursal').val()
        })
        ajax_call('portal_marcaciones_insert', {
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

$('#extraer').click(function () {
    ajax_call('portal_marcaciones_extraer', {
            _xsrf: getCookie("_xsrf")
        }, null, function () {
            setTimeout(function () {
            window.location = main_route
        }, 2000);
    })

})


function attach_edit() {
    $('.edit').click(function () {
        obj = JSON.stringify({
            'id': parseInt(JSON.parse($(this).attr('data-json')))
        })
        ajax_call_get('portal_marcaciones_update', {
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
        ajax_call('portal_marcaciones_update', {
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
        title: "¿Desea dar de baja los datos de la empresa?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#1565c0",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    }).then(function () {
        ajax_call('portal_marcaciones_delete', {
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


$('#filtrar').click(function () {
    $("#rgm-loader").show();
    document.getElementById("filtrar").disabled = true
    obj = JSON.stringify({
        'fechainicio': $('#fechainicio').val(),
        'fechafin': $('#fechafin').val(),
        '_xsrf': getCookie("_xsrf")
    })
    ruta = "portal_marcaciones_filtrar";
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