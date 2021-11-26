main_route = '/marcaciones'

$(document).ajaxStart(function () { });

$(document).ajaxStop(function () {
    $.Toast.hideToast();
});

var fechahoy = new Date()
var hoy = fechahoy.getDate()+"/"+(fechahoy.getMonth()+1) +"/"+fechahoy.getFullYear()

document.getElementById("fechai").value=hoy
document.getElementById("fechaf").value=hoy

$('.show-tick').selectpicker()


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

$('#importar_marcaciones').click(function () {
    $(".xlsfl").each(function () {
        $(this).fileinput('refresh',{
            allowedFileExtensions: ['xlsx', 'xls', 'txt'],
            maxFileSize: 10000,
            maxFilesNum: 1,
            showUpload: false,
            layoutTemplates: {
                main1: '{preview}\n' +
                    '<div class="kv-upload-progress hide"></div>\n' +
                    '<div class="input-group {class}">\n' +
                    '   {caption}\n' +
                    '   <div class="input-group-btn">\n' +
                    '       {remove}\n' +
                    '       {cancel}\n' +
                    '       {browse}\n' +
                    '   </div>\n' +
                    '</div>',
                main2: '{preview}\n<div class="kv-upload-progress hide"></div>\n{remove}\n{cancel}\n{browse}\n',
                preview: '<div class="file-preview {class}">\n' +
                    '    {close}\n' +
                    '    <div class="{dropClass}">\n' +
                    '    <div class="file-preview-thumbnails">\n' +
                    '    </div>\n' +
                    '    <div class="clearfix"></div>' +
                    '    <div class="file-preview-status text-center text-success"></div>\n' +
                    '    <div class="kv-fileinput-error"></div>\n' +
                    '    </div>\n' +
                    '</div>',
                icon: '<span class="glyphicon glyphicon-file kv-caption-icon"></span>',
                caption: '<div tabindex="-1" class="form-control file-caption {class}">\n' +
                    '   <div class="file-caption-name"></div>\n' +
                    '</div>',
                btnDefault: '<button type="{type}" tabindex="500" title="{title}" class="{css}"{status}>{icon}{label}</button>',
                btnLink: '<a href="{href}" tabindex="500" title="{title}" class="{css}"{status}>{icon}{label}</a>',
                btnBrowse: '<div tabindex="500" class="{css}"{status}>{icon}{label}</div>',
                progress: '<div class="progress">\n' +
                    '    <div class="progress-bar progress-bar-success progress-bar-striped text-center" role="progressbar" aria-valuenow="{percent}" aria-valuemin="0" aria-valuemax="100" style="width:{percent}%;">\n' +
                    '        {percent}%\n' +
                    '     </div>\n' +
                    '</div>',
                footer: '<div class="file-thumbnail-footer">\n' +
                    '    <div class="file-caption-name" style="width:{width}">{caption}</div>\n' +
                    '    {progress} {actions}\n' +
                    '</div>',
                actions: '<div class="file-actions">\n' +
                    '    <div class="file-footer-buttons">\n' +
                    '        {delete} {other}' +
                    '    </div>\n' +
                    '    {drag}\n' +
                    '    <div class="file-upload-indicator" title="{indicatorTitle}">{indicator}</div>\n' +
                    '    <div class="clearfix"></div>\n' +
                    '</div>',
                actionDelete: '<button type="button" class="kv-file-remove {removeClass}" title="{removeTitle}"{dataUrl}{dataKey}>{removeIcon}</button>\n',
                actionDrag: '<span class="file-drag-handle {dragClass}" title="{dragTitle}">{dragIcon}</span>'
            }
        })
    });
    verif_inputs('')

    $('#id_div').hide()
    $('#insert_importar').show()
    $('#update').hide()
    $('#form').modal('show')
})

$('#importar-form').on('submit', function (e) {
    $('.page-loader-wrapper').show();
    var data = new FormData($(this)[0]);
    data.append('_xsrf', getCookie("_xsrf"))

    $.ajax({
        url: 'marcaciones_importar',
        type: "post",
        data: data,
        contentType: false,
        processData: false,
        cache: false
    }).done(function (response) {

        $('.page-loader-wrapper').hide();
        $('#form').modal('hide');
        response = JSON.parse(response)

        if (response.success) {
            swal({
                title: "Operacion Correcta...",
                text: response.message,
                type: "success",
                showCancelButton: false,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "Confirmar"
            }).then(function () {
                $('#form-importar').modal('hide')
                setTimeout(function () {
                    window.location = main_route
                }, 500);
            });
        } else {
            swal("Operacion Fallida", response.message, "error").then(function () {
                query_render('/marcaciones');
            });
        }
    });
    e.preventDefault();
});


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
        ajax_call('marcaciones_insert', {
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
    ajax_call('marcaciones_extraer', {
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
        ajax_call_get('marcaciones_update', {
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
        ajax_call('marcaciones_update', {
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
        ajax_call('marcaciones_delete', {
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
                'fechainicio': $('#fechai').val(),
                'fechafin': $('#fechaf').val(),
                '_xsrf': getCookie("_xsrf")
            })
            ruta = "marcaciones_filtrar";
            $.ajax({
                method: "POST",
                url: ruta,
                data: {_xsrf: getCookie("_xsrf"), object: obj},
                async: true
            }).done(function (response) {
                response = JSON.parse(response)

                var data = [];
                for (var i = 0; i < Object.keys(response.response).length; i++) {
                    //console.log(i)
                    data.push( [
                        response['response'][i]["id"], response['response'][i]["codigo"], response['response'][i]["nombre"],
                        response['response'][i]["fecha"],response['response'][i]['hora'], response['response'][i]['dispositivo']
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
                           title: 'Marcaciones Registradas'  },
                        {  extend : 'pdfHtml5',
                           customize: function(doc) {
                                doc.styles.tableBodyEven.alignment = 'center';
                                doc.styles.tableBodyOdd.alignment = 'center';
                           },
                           exportOptions : {
                                columns : [0, 1, 2, 3, 4, 5]
                            },
                           title: 'Marcaciones Registradas'
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
            })
        });
