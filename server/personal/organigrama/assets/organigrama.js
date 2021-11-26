main_route = '/organigrama'

var gb_selectnd = null;
var gb_idpnd = null;

$(document).ready(function(){
    
    function buildDOM(tree) {
        function buildLI(node) {
            var li = document.createElement('li'),
                    a = document.createElement('a');
            a.href = node.url;
            a.appendChild(document.createTextNode(node.name));
            li.appendChild(a);
            if (node.children.length > 0) {
                var ul = document.createElement('ul');
                while (node.children.length > 0) {
                    x1 = node.children.pop()
                    ul.appendChild(buildLI(x1));
                }
                li.appendChild(ul);
            }
            return li;
        }
    
        var ul = document.createElement('ul');
        while (tree.children.length > 0) {
            x = tree.children.pop();
            ul.append(buildLI(x));
        }
        return ul;
    }
    
    $.ajax({
        method: "POST",
        url: '/organigrama_data',
        data: {_xsrf: getCookie("_xsrf")},
        async: false
    }).done(function (response) {
        datascource = JSON.parse(response)
        datascource = datascource.response;
    })


    var getId = function () {
        return (new Date().getTime()) * 1000 + Math.floor(Math.random() * 1001);
    };
    i = 0;

    $('#pluginsorg').orgchart({
        'data': datascource,
        'nodeContent': 'title',
        'draggable': true,
        'verticalDepth': 4,
        'dropCriteria': function ($draggedNode, $dragZone, $dropZone) {
            if ($draggedNode.find('.content').text().indexOf('manager') > -1 && $dropZone.find('.content').text().indexOf('engineer') > -1) {
                return false;
            }
            return true;
        }
    })
    .on('click', '.node', function () {
        var $this = $(this);

        //gb_selectnd = $this.attr('id')

        $('#node_parent_id').val($this.attr('id')).data('node', $this);
        var data = JSON.stringify({
            'fkpadre': parseInt($this.attr('data-parent')),
            'id': parseInt($this.attr('id'))
        })
        console.log(data)
        ajax_call('/organigrama_get_brother', {object: data, _xsrf: getCookie("_xsrf")}, null, function (response) {
            response=JSON.parse(response)
            datanew = response.response;
        })
    })
    .on('click', '.orgchart', function (event) {
        if (!$(event.target).closest('.node').length) {
            $('#node_parent_id').val('');
        }
    }).children('.orgchart').on('nodedropped.orgchart', function (event) {
        objeto = JSON.stringify({
            'parent': parseInt(event.dropZone.attr('id')),
            'id': parseInt(event.draggedNode.attr('id'))
        })
        ajax_call("/organigrama_update", {object: objeto, _xsrf: getCookie("_xsrf")}, null, null)

        window.location = main_route
        //query_render("feriado")
    });
    $('.orgchart').addClass('noncollapsable');
});

$('#fkpersona').selectpicker({
    size: 4,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar Empleado',
    title: 'Seleccione un Empleado'

})

$('#fkcargo').selectpicker({
    size: 4,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar Cargo',
    title: 'Seleccione un Cargo'
})

$('#siguiente').selectpicker({
    size: 4,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar Posición',
    title: 'Seleccione un Posición'
})

    $('#fkcargo').change(function () {
        cargar_persona(parseInt($('#fkcargo').val()))

    });


    function cargar_persona(fkcargo) {
        obj = JSON.stringify({
            'idcargo': fkcargo,
            '_xsrf': getCookie("_xsrf")
        })

        ruta = "persona_obtener_x_cargo";
        //data.append('object', obj)
        //data.append('_xsrf',getCookie("_xsrf"))
        $.ajax({
            method: "POST",
            url: ruta,
            data: {_xsrf: getCookie("_xsrf"), object: obj},
            async: false
        }).done(function (response) {
            response = JSON.parse(response)
            $('#fkpersona').html('');
            var select = document.getElementById("fkpersona")
            for (var i = 0; i < Object.keys(response.response).length; i++) {
                var option = document.createElement("OPTION");
                option.innerHTML = response['response'][i]['fullname'];
                option.value = response['response'][i]['id'];
                select.appendChild(option);
            }
            $('#fkpersona').selectpicker('refresh');

        })


    }

$('#new').click(function () {
    if ($('.node.focused').length > 0) {
        $('#id').val('')
        $('#id_div').hide()
        $('#insert').show()
        $('#update').hide()

        $('#fkcargo').val('').selectpicker('refresh')
        $('#fkpersona').val('').selectpicker('refresh')
        $('#href').val("")
        $('#siguiente option').filter(function () {
            return this.value != ''
        }).remove()
        $('#siguiente').selectpicker('refresh')
        var opcion = "";
        for (var i = 1; i <= datanew.contador_son + 1; i++) {
            opcion = opcion + "<option value='" + i + "'>" + i + "</option>";
        }
        $('#siguiente').append(opcion).selectpicker('refresh')
        clean_form()
        verif_inputs()
        $('#form').modal('show')
    } else {
        showMessage('Elegir un Nodo Padre', "warning", "ok")
    }
})


function item_is_empty(items){
    for (ic = 0; ic < items.length; ic++) {
        if(items[ic] == ''){
            return true;
        }
    }
    return false;
}

function valid_dataform(){
    var object_inputs = $('.orgcomp')
    console.log(object_inputs)

    h1 = object_inputs[1].value;
    h2 = object_inputs[3].value;
    h3 = object_inputs[5].value;

    items = [h1, h2, h3];
    resp = !item_is_empty(items);

    return resp;
}

$('#insert').click(function () {
    if (Object.keys(datascource).length > 1 && $('#node_parent_id').val() === '') {
        showMessage('Elegir Padre para esta categoria', "danger", "remove")
        return
    }

    objeto = JSON.stringify({
        'fkpadre': parseInt($('#node_parent_id').val()),
        'fkcargo': $('#fkcargo').val(),
        'fkpersona': $('#fkpersona').val(),
        'siguiente': $('#siguiente').val(),
        'gerencia': document.getElementById('gerencia').checked,
        'jefatura': document.getElementById('jefatura').checked
    })
    $('body').removeClass('modal-open')
    $('.modal-backdrop').remove();

    if(valid_dataform()){
        ajax_call('organigrama_insert', {
            object: objeto,
            _xsrf: getCookie("_xsrf")
        }, null, function () {
            $('#form').modal('hide')
            setTimeout(function () {
                window.location = main_route
            }, 1500)
        });
    }else{
        swal(
            'Error',
            'Ingrese todos los datos requeridos.',
            'warning'
        )
    }
})


/*$('#edit').click(function () {
    $('#insert').hide()
    $('#update').show()
    $('#form').modal('show')
})*/

$('#delete').click(function () {
    if (Object.keys(datascource).length > 0 && $('#node_parent_id').val() === '') {
        showMessage('Elija una nodo', "danger", "remove");
        return
    }

    objeto = JSON.stringify({
        'id': parseInt($('#node_parent_id').val()),
    });
    idmm = parseInt($('#node_parent_id').val());
    if (idmm != 1) {
        ajax_call('organigrama_delete', {
            object: objeto,
            _xsrf: getCookie("_xsrf")
        }, null, function () {
           // window.location = main_route
            setTimeout(function () {
                window.location = main_route
            }, 1500)
        });
    } else {
        showMessage('Error no puede eliminar raiz', "danger", "remove");
    }
})

$('#edit').click(function () {
    if ($('.node.focused').length > 0) {
        objeto = JSON.stringify({
            'id': parseInt($('.node.focused').prop('id')),
        })
        idm = parseInt($('.node.focused').prop('fkpadre'))
        console.log(idm)
        if (idm != 1) {
            ajax_call("/organigrama_get", {object: objeto, _xsrf: getCookie("_xsrf")}, null, function (response) {
                data = JSON.parse(response)
                self = data.response
                if (self.id != 1) {
                    $('#node_parent_id').hide();
                    $('.cmb').selectpicker('val', self.fkcargo);
                    $('.cmb').selectpicker('val', self.fkpersona);
                    $('.cmb').each(function (cmb) {
                        $("#cmb")
                    })

                    $('#node_id').val(self.id);
                    $('#node_parent_id').val(self.fkpadre);
                    gb_idpnd = self.fkpadre
                    cargar_persona(self.fkcargo)


                    $('#fkcargo').val(self.fkcargo);
                    $('#fkpersona').val(self.fkpersona);
                    document.getElementById('gerencia').checked=self.gerencia
                    document.getElementById('jefatura').checked=self.jefatura
                    $('#id_div').hide();
                    $('#insert').hide()
                    $('#update').show()
                    ;
                    clean_form()
                    verif_inputs()
                    $('#form').modal('show');

                    $('#siguiente option').filter(function () {
                        return this.value != ''
                    }).remove()
                    $('#siguiente').selectpicker('refresh')
                    $('#fkcargo').selectpicker('refresh')
                    $('#fkpersona').selectpicker('refresh')
                    var opcion = "";
                    for (var i = 1; i <= datanew.contador_bro; i++) {
                        opcion = opcion + "<option value='" + i + "'>" + i + "</option>";
                    }
                    $('#siguiente').append(opcion).selectpicker('refresh')
                    $('#siguiente').selectpicker('val', self.siguiente);
                } else {
                    showMessage('No se puede modificar la raiz', "warning", "ok")
                }
            })
        } else {
            showMessage('No se puede modificar la raiz', "warning", "ok")
        }
    } else {
        showMessage('Elegir un Nodo', "warning", "ok")
    }
})

$('#update').click(function () {
    if (Object.keys(datascource).length > 1 && $('#node_parent_id').val() === '') {
        showMessage('Elegir Padre para esta categoria', "danger", "remove")
        return
    }

    objeto = JSON.stringify({
        'id': parseInt($('#node_id').val()),
        'fkpadre': parseInt($('#node_parent_id').val()),
        'fkcargo': $('#fkcargo').val(),
        'fkpersona': $('#fkpersona').val(),
        'siguiente': $('#siguiente').val(),
        'gerencia': document.getElementById('gerencia').checked,
        'jefatura': document.getElementById('jefatura').checked
    })
    $('body').removeClass('modal-open')
    $('.modal-backdrop').remove();
    if(valid_dataform()){
        ajax_call("/organigrama_edit", {object: objeto, _xsrf: getCookie("_xsrf")}, null, function () {
            $('#form').modal('hide')
            setTimeout(function () {
                window.location = main_route
            }, 1500)
        });
    }else{
        swal(
            'Error',
            'Ingrese todos los datos requeridos.',
            'warning'
        )
    }
})

    $('#reporte-xls').click(function () {
        aux = {'datos': ''}
        obj = JSON.stringify(aux)
        ruta = "/organigrama_reporte_xls";
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

    ruta = "organigrama_importar";
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

// Evitar que el nodo padre se todo pueda editarse o eliminarse
$(document).ready(function(){
    let nodo_padre = document.getElementsByTagName("tbody");
    let hijo_tr = nodo_padre[0].firstChild;
    let deshabilitar = setInterval(myTimer, 500);
    let botonEditar = document.getElementById("edit");
    let botonEliminar = document.getElementById("delete");
    let hijo_div = hijo_tr.firstChild.firstChild;
    function myTimer() {
        if (hijo_div.classList.contains("focused")){
            botonEditar.removeAttribute("enabled");
            botonEditar.setAttribute("disabled", " ");
            botonEliminar.removeAttribute("enabled");
            botonEliminar.setAttribute("disabled", " ");
        }else{
            botonEditar.removeAttribute("disabled");
            botonEditar.setAttribute("enabled", " ");
            botonEliminar.removeAttribute("disabled");
            botonEliminar.setAttribute("enabled", " ");
        }
    }
});