main_route = "/menu"


$(".hr").inputmask("h:s",{ "placeholder": "__/__" });

document.getElementById("primero").click();

$('#tipo_platos').selectpicker({
    size: 7,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar opción',
    title: 'Seleccione un tipo de plato'
})

function obtener_platos() {
    hours = []
    hours_inputs = $('.plato')

    for(i=0;i<hours_inputs.length;i+=2){
        h0 = hours_inputs[i].value;
        h1 = hours_inputs[i + 1].value;

        hours.push((function add_hours(h0,h1) {

            if (h0 == ''){
                return {
                    'fkplato': h1
                }
            }else{
                return {
                'id':h0,
                'fkplato': h1
                }
            }
        })(
            hours_inputs[i].value,
            hours_inputs[i+1].value)
        )
    }
    return hours
}

$(".file").each(function () {
            $(this).fileinput('refresh', {
                allowedFileExtensions: ['jpg', 'gif', 'jpeg', 'png', 'ico', 'webp'],
                maxFileSize: 20000,
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

    $('#primero').click(function () {
        $('#body-cont').css("display", "block")
        $('#body-elfec').css("display", "none")
    })

    $('#segundo').click(function () {
        $('#body-cont').css("display", "none")
        $('#body-elfec').css("display", "block")
    })

$('#new').click(function () {
    $('#nombre_platos').val('')
    $('#tipo_platos').val('')
    $('#tipo_platos').selectpicker('refresh')

    verif_inputs('')
    $('#id_div_platos').hide()
    $('#insert_platos').show()
    $('#update_platos').hide()
    validationInputSelects("form_platos");
    $('#form_platos').modal('show')
})

$('#insert').on('click',function (e) {
     e.preventDefault();
    var data = new FormData($('#form_submit')[0]);
    fecha_inicial = moment($('#fecha_ini').val()+"/"+ new Date().getFullYear() ,"DD/MM/YYYY")
    fecha_final = moment($('#fecha_fin').val()+"/"+ new Date().getFullYear() ,"DD/MM/YYYY")
        notvalid = validationInputSelectsWithReturn("form");
    if (notvalid===false) {
        objeto = JSON.stringify({
             'nombre': $('#nombre').val(),
             'fecha': $('#fecha').val(),
             'menuplato': obtener_platos()
        })
        ruta = "menu_insert";
        data.append('object', objeto)
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
            if (render != null) {
                $(render).html(response)
            } else {
                dictionary = JSON.parse(response)
                if ("message" in dictionary && dictionary.message != '') {
                    if (dictionary.success) {
                        showMessage(dictionary.message, "success", "ok")
                    } else {
                        showMessage(dictionary.message, "danger", "remove")
                    }
                }
            }
            if (callback != null) {
                callback(response)
            }
        })
        $('#form').modal('hide')
    }else {
        swal(
            'Error de datos.',
            notvalid,
            'error'
        )
    }

})

$('#insert_platos').click(function () {
    notvalid = validationInputSelectsWithReturn("form_platos");
    if (notvalid===false) {
        objeto = JSON.stringify({
            'nombre': $('#nombre_platos').val(),
            'tipo': $('#tipo_platos').val()
        })
        ajax_call('menu_plato_insert', {
            object: objeto,
            _xsrf: getCookie("_xsrf")
        }, null, function () {
            setTimeout(function () {
                window.location = main_route
            }, 2000);
        })
        $('#form_platos').modal('hide')
    } else {
        swal(
            'Error de datos.',
            notvalid,
            'error'
        )
    }
})

$('#update').on('click',function (e) {
     e.preventDefault();
    var data = new FormData($('#form_submit')[0]);
    fecha_inicial = moment($('#fecha_ini').val()+"/"+ new Date().getFullYear() ,"DD/MM/YYYY")
    fecha_final = moment($('#fecha_fin').val()+"/"+ new Date().getFullYear() ,"DD/MM/YYYY")
    objeto = JSON.stringify({
         'id': $('#id').val(),
         'nombre': $('#nombre').val(),
         'fecha': $('#fecha').val(),
         'menuplato': obtener_platos()
    })
    ruta = "menu_update";
    data.append('object', objeto)
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
        if (render != null) {
            $(render).html(response)
        } else {
            dictionary = JSON.parse(response)
            if ("message" in dictionary && dictionary.message != '') {
                if (dictionary.success) {
                    showMessage(dictionary.message, "success", "ok")
                } else {
                    showMessage(dictionary.message, "danger", "remove")
                }
            }
        }
        if (callback != null) {
            callback(response)
        }
    })
    $('#form').modal('hide')

})

$('#delete').on('click',function (e) {
     e.preventDefault();
    var data = new FormData($('#form_submit')[0]);
    fecha_inicial = moment($('#fecha_ini').val()+"/"+ new Date().getFullYear() ,"DD/MM/YYYY")
    fecha_final = moment($('#fecha_fin').val()+"/"+ new Date().getFullYear() ,"DD/MM/YYYY")
    objeto = JSON.stringify({
         'id': $('#id').val()
    })
    ruta = "menu_delete";
    data.append('object', objeto)
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
        if (render != null) {
            $(render).html(response)
        } else {
            dictionary = JSON.parse(response)
            if ("message" in dictionary && dictionary.message != '') {
                if (dictionary.success) {
                    showMessage(dictionary.message, "success", "ok")
                } else {
                    showMessage(dictionary.message, "danger", "remove")
                }
            }
        }
        if (callback != null) {
            callback(response)
        }
    })
    $('#form').modal('hide')

})



function attach_edit() {
    $('.edit').click(function () {
        obj = JSON.stringify({
            'id': parseInt(JSON.parse($(this).attr('data-json')))
        })

        ajax_call_get('menu_update', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            $('#id').val(self.id)
            $('#nombre').val(self.nombre)
            $('#fecha').val(self.fecha)
            $('.nfoto').show()

            if (self.foto != "None" && self.foto != "") {
                document.getElementById("imagen_show_img").src = self.foto;
            } else {
                document.getElementById("imagen_show_img").src = "/resources/images/sinImagen.jpg";
            }

            clean_form()
            verif_inputs('')
            $('#id_div').hide()
            $('#insert').hide()
            $('#update').show()
            $('#form').modal('show')
        })
    })

    $('.edit_platos').click(function () {
        obj = JSON.stringify({
            'id': parseInt(JSON.parse($(this).attr('data-json')))
        })

        ajax_call_get('menu_plato_update', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            $('#id_platos').val(self.id)
            $('#nombre_platos').val(self.nombre)
            $('#tipo_platos').val(self.tipo)
            $('#tipo_platos').selectpicker('refresh')

            clean_form()
            verif_inputs('_platos')
            $('#id_div_platos').hide()
            $('#insert_platos').hide()
            $('#update_platos').show()
            validationInputSelects("form")
            $('#form_platos').modal('show')
        })
    })

    $('#edit_hora').click(function () {

        objeto = JSON.stringify({
            'horaLimite': $('#horaLimite').val(),
            'horaInicio': $('#horaInicio').val(),
            'horaFin': $('#horaFin').val()

        })
        ajax_call('menu_hora', {
            object: objeto,
            _xsrf: getCookie("_xsrf")
        }, null, function () {
            setTimeout(function () {
                window.location = main_route
            }, 2000);
        })

})

    $('.estado_platos').click(function (e) {
        e.preventDefault()
        cb_delete = this
        b = $(this).prop('checked')
        if (!b) {
            cb_title = "¿Está seguro de que desea deshabilitar?"

        } else {
            cb_title = "¿Está seguro de que desea habilitar?"
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
            objeto = JSON.stringify({
                id: parseInt($(cb_delete).attr('data-id')),
                enabled: $(cb_delete).is(':checked')
            })

            ajax_call("menu_plato_estado", {
                object: objeto,
                _xsrf: getCookie("_xsrf")
            }, null, function () {

            })
            $('#form').modal('hide')
        })
    })
}
attach_edit()

$('#update_platos').click(function () {
    notvalid = validationInputSelectsWithReturn("form");
    if (notvalid===false) {
        objeto = JSON.stringify({
            'id': parseInt($('#id_platos').val()),
            'nombre': $('#nombre_platos').val(),
            'tipo': $('#tipo_platos').val()
        })
        ajax_call('menu_plato_update', {
            object: objeto,
            _xsrf: getCookie("_xsrf")
        }, null, function () {
            setTimeout(function () {
                window.location = main_route
            }, 2000);
        })
        $('#form_platos').modal('hide')
    } else {
        swal(
            'Error de datos.',
            notvalid,
            'error'
        )
    }
})
reload_form()

validationKeyup("form");
validationSelectChange("form");