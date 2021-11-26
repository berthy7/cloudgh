main_route = '/turno'

$(document).ready(function () {
    $('#data_table').DataTable();
});

$(document).ajaxStart(function () { });

$(document).ajaxStop(function () {
    $.Toast.hideToast();
});




function agregar_turno(id_in) {
    $('#turno_div').append(
        '<div class="row">\
            <div class="col-md-2" hidden>\
                <div class="form-group form-float">\
                    <div class="form-line">\
                        <input id="id'+id_in+'" data-id="'+id_in+'" class="form-control id horas" readonly>\
                        <label class="form-label">Id</label>\
                    </div>\
                </div>\
            </div>\
            <div class="col-md-3">\
                <b>Entrada</b>\
                <div class="input-group">\
                    <span class="input-group-addon"><i class="material-icons">access_time</i></span>\
                    <div class="form-line"><input id="entrada_'+id_in+'" name="Entrada" type="text" class="form-control horas hr" placeholder="Ex: 23:59"  required></div>\
                </div>\
            </div>\
            <div class="col-md-3">\
                <b>Salida</b>\
                <div class="input-group">\
                    <span class="input-group-addon"><i class="material-icons">access_time</i></span>\
                    <div class="form-line"><input id="salida_'+id_in+'" name="Salida" type="text" class="form-control horas hr" placeholder="Ex: 23:59" required></div>\
                </div>\
            </div>\
            <div class="col-md-3">\
                <button type="button" class="btn bg-deep-purple waves-effect borrar_turno">\
                    <i class="material-icons">clear</i>\
                </button>\
            </div>\
        </div>'
    )
    $('.borrar_turno').last().click(function () {
        $(this).parent().parent().remove()
    })

    $(".hr").inputmask("h:s",{ "placeholder": "__/__" });
    inputmask_keyup()
}

$('#nuevo_turno').click(function () {
    agregar_turno('')
})

function obtener_turno() {
    objeto = []
    objeto_clase = $('.horas')

    console.log(objeto_clase)

    for(i=0;i<objeto_clase.length;i+=3){
        h0 = obtener_segundos(objeto_clase[i].value)
        h1= obtener_segundos(objeto_clase[i+1].value)
        h2 = obtener_segundos(objeto_clase[i+2].value)


        objeto.push((function add_objeto(h0, h1, h2) {
            if (h0 ==''){
                return {
                    'entrada': h1,
                    'salida': h2
                }
            }else{
                return {
                    'id': h0,
                    'entrada': h1,
                    'salida': h2
                    }
            }
        })(
            objeto_clase[i].value,
            objeto_clase[i+1].value,
            objeto_clase[i+2].value)
        )
    }
    return objeto
}

function obtener_segundos(hora) {
    hm = hora.split(':')
    sec = (parseInt(hm[0])*3600) + (parseInt(hm[1])*60)
    return sec
}


$('#new').click(function () {
    $('#id').val('')
    $('#nombre').val('')
    $('#codigo').val('')
    $('#turno_div').empty()
    agregar_turno('')

    verif_inputs('')
    $('#id_div').hide()
    $('#insert').show()
    $('#update').hide()
    validationInputSelects("form")
    $('#form').modal('show')
    $('#nombre').parent().addClass('focus focused')



})


$('#insert').click(function () {
    hora = validarLongitudHora("turno_div");
    // horaValida = validarHorarios("turno_div");
    if (hora===true) {
        notvalid = validationInputSelectsWithReturn("form");
        if (notvalid===false) {
                objeto = JSON.stringify({
                    'nombre': $('#nombre').val(),
                    'codigo': $('#codigo').val(),
                    'hora': obtener_turno()
                })

                ajax_call('turno_insert', {
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
            'Error de datos.',
            notvalid,
            'error'
             )
        }

    } else {
        swal(
            'Error de datos.',
            'Ingrese la hora correctamente',
            'error'
        )
    }
})

$('#sms').click(function () {
    console.log("h")
     $('#id').val('')
    $('#telefeno').val('')
    $('#texto').empty()


    verif_inputs('')
    $('#insert-sms').show()

    validationInputSelects("form")
    $('#form-sms').modal('show')
})

$('#insert_sms').click(function () {

    objeto = JSON.stringify({
        'telefono': $('#telefono').val(),
        'texto': $('#texto').val()
    })

    ajax_call('turno_sms', {
        object: objeto,
        _xsrf: getCookie("_xsrf")
    }, null, function () {
        setTimeout(function () {
            window.location = main_route
        }, 2000);
    })
    $('#form-sms').modal('hide')

})


function attach_edit() {
    $('.edit').click(function () {
        obj = JSON.stringify({
            'id': parseInt(JSON.parse($(this).attr('data-json')))
        })

        ajax_call_get('turno_update', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            console.log(self)
            $('#id').val(self.id)
            $('#nombre').val(self.nombre)
            $('#codigo').val(self.codigo)

            $('#turno_div').empty()

            for(i in self.hora){
                aux0 = self.hora[i].id
                aux1 = self.hora[i].entrada
                aux2= self.hora[i].salida

                agregar_turno(aux0)
                $('#id'+aux0).val(aux0)
                $('#entrada_'+aux0).val(aux1)
                $('#salida_'+aux0).val(aux2)
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


$('#update').click(function () {

    hora = validarLongitudHora("turno_div");
    // horaValida = validarHorarios("turno_div");
    if (hora===true) {
        notvalid = validationInputSelectsWithReturn("form");
        if (notvalid===false) {
                objeto = JSON.stringify({
                    'id': $('#id').val(),
                    'nombre': $('#nombre').val(),
                    'codigo': $('#codigo').val(),
                    'hora': obtener_turno()
                })

                ajax_call('turno_update', {
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
            'Error de datos.',
            notvalid,
            'error'
             )
        }

    } else {
        swal(
            'Error de datos.',
            'Ingrese la hora correctamente',
            'error'
        )
    }
})
reload_form()


$('.delete').click(function () {
    id = parseInt(JSON.parse($(this).attr('data-json')))
    enabled = false

    swal({
        title: "¿Desea dar de baja el turno?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#1565c0",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    }).then(function () {
        ajax_call('turno_delete', {
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

    $('#reporte-xls').click(function () {
        aux = {'datos': ''}
        obj = JSON.stringify(aux)
        ruta = "/turno_reporte_xls";
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

    $('#importar_Excel').click(function () {
    $(".xlsfl").each(function () {
        $(this).fileinput('refresh',{
            allowedFileExtensions: ['xlsx', 'txt'],
            maxFileSize: 2000,
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
        console.log("importar excel")

    $('#id_div').hide()
    $('#insert-importar').show()
    $('#form-importar').modal('show')
})

    $('#insert-importar').on('click',function (e) {
     e.preventDefault();

    var data = new FormData($('#importar-form')[0]);

    ruta = "turno_importar";
    data.append('_xsrf', getCookie("_xsrf"))
    render = null
    callback = function () {
        setTimeout
        (function () {
            window.location = main_route
        }, 2000);
    }
    $.ajax({
        url: ruta,
        type: "post",
        data: data,
        contentType: false,
        processData: false,
        cache: false,
        async: false
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
                query_render('/residente');
            });
        }
    })
    $('#form').modal('hide')
})

validationKeyup("form");
validationSelectChange("form");
