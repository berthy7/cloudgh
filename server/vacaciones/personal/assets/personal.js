main_route = '/v_personal'

$(document).ready(function () {
    $('#data_table').DataTable();
});

$(document).ajaxStart(function () { });

$(document).ajaxStop(function () {
    $.Toast.hideToast();
});

var fechahoy = new Date();
console.log(fechahoy)
var hoy = fechahoy.getDate()+"/"+(fechahoy.getMonth()+1) +"/"+fechahoy.getFullYear()


document.getElementById("fechaiboleta").value=hoy
document.getElementById("fechafboleta").value=hoy

$('.show-tick').selectpicker()

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
            return a
        })(a))
    })
    return aux
}

function obtener_personas() {
    objeto = []
    objeto_inputs = $('.personal')

    for (i = 0; i < objeto_inputs.length; i += 1) {
        h0 = parseInt(objeto_inputs[i].value)

        objeto.push((function add_objeto(h0) {
                return h0
        })(h0))
    }
    return objeto
}

$('#estado').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar ',
    title: 'Seleccione un estado'
})
$('#boleta').click(function () {

    $('#fechaiboleta').val($('#fechai').val())
    $('#fechafboleta').val($('#fechaf').val())
    $('#personal_div').empty()
    $('#desplegable').show()
    $('#cliente_title').html('Descargar Reportes de Vacacion')
    $('#aclaracion').hide()
    $('#generar_pdf').show()
    $('#generar_rep').show()
    $('#eliminar_reg').hide()
    $('#form-boleta').modal('show')
})

$('#generar_rep').click(function () {
    obj = JSON.stringify({
        'fechainicio': $('#fechaiboleta').val(),
        'fechafin': $('#fechafboleta').val(),
        'personas_arbol': obtener_personas_arbol(),
        'personas': obtener_personas(),
        '_xsrf': getCookie("_xsrf")
    })

    $.ajax({
        method: "POST",
        url: '/v_personal_reporte_total',
        data: {object: obj, _xsrf: getCookie("_xsrf")}
    }).done(function(response){
        dictionary = JSON.parse(response)
        dictionary = dictionary.response
        servidor = ((location.href.split('/'))[0])+'//'+(location.href.split('/'))[2];
        url = servidor + dictionary;

        window.open(url)
    })
})


$('#importar_excel').click(function () {
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

    $('#id_div').hide()
    $('#insert-importar').show()
    $('#form-importar').modal('show')
})

$('#insert-importar').on('click',function (e) {
     e.preventDefault();

    var data = new FormData($('#importar-form')[0]);

    ruta = "v_personal_importar";
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

$('#new').click(function () {
    $('#nombre').val('')
    $('#fkciudad').val('')
    $('#fkciudad').selectpicker('refresh')

    verif_inputs('')
    $('#id_div').hide()
    $('#insert').show()
    $('#update').hide()
    validationInputSelects("form")
    $('#form').modal('show')
})


$('#insert').click(function () {
    notvalid = validationInputSelectsWithReturn("form");
    if (notvalid===false) {
        objeto = JSON.stringify({
            'nombre': $('#nombre').val(),
            'fkciudad': $('#fkciudad').val()
        })
        ajax_call('v_personal_insert', {
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


function attach_edit() {
    $('.edit').click(function () {
        obj = JSON.stringify({
            'id': parseInt(JSON.parse($(this).attr('data-json')))
        })
        ajax_call_get('v_personal_update', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            $('#id').val(self.id)
            $('#nombre').val(self.persona.fullname)
            $('#dias').val(self.dias)
            $('#gestion').val(self.gestion)
            $('#estado').val(self.estado)
            $('#estado').selectpicker('refresh')


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
    notvalid = validationInputSelectsWithReturn("form");
    if (notvalid===false) {
        objeto = JSON.stringify({
            'id': parseInt($('#id').val()),
            'dias': $('#dias').val(),
            'gestion': $('#gestion').val(),
            'estado': $('#estado').val()

        })
        ajax_call('v_personal_update', {
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

 $('.historico').click(function () {
    obj = JSON.stringify({
        'fkpersona': parseInt(JSON.parse($(this).attr('data-fkpersona'))),
        '_xsrf': getCookie("_xsrf")
    })

    $.ajax({
        method: "POST",
        url: '/v_personal_historico',
        data: {object: obj, _xsrf: getCookie("_xsrf")}
    }).done(function(response){
        dictionary = JSON.parse(response)
        dictionary = dictionary.response
        servidor = ((location.href.split('/'))[0])+'//'+(location.href.split('/'))[2];
        url = servidor + dictionary;

        window.open(url)
    })
})

validationKeyup("form");
validationSelectChange("form");