main_route = '/rol'

$(document).ready( function () {
    $('#data_table').DataTable();
});
validationKeyup("form")

function analizar(parent) {
    children = $(parent).next().next().find('.module:checked')
    $(parent).prop('checked', (children.length > 0))
    grand_parent = $(parent).parent().closest('.tree-feriado').prev().prev()
    if (grand_parent.length > 0){
        analizar(grand_parent)
    }
}

$('.module').click(function () {
    aux = $(this).attr('id')
    if((aux.indexOf('insert')!==-1 || aux.indexOf('update')!==-1 || aux.indexOf('delete')!==1) && $(this).is(':checked')){
        aux1 = aux.replace('insert', 'query')
        aux1 = aux1.replace('update', 'query')
        aux1 = aux1.replace('delete', 'query')
        $('#'+aux1).prop('checked', true)
    }

    if(aux.indexOf('query')!==-1){
        aux1 = aux.replace('query', 'insert')
        $('#'+aux1).prop('checked', false)
        aux1 = aux.replace('query', 'update')
        $('#'+aux1).prop('checked', false)
        aux1 = aux.replace('query', 'delete')
        $('#'+aux1).prop('checked', false)
    }

    $(this).next().next().find('.module').prop('checked', $(this).prop('checked'))
    analizar($(this).parent().closest('.tree-feriado').prev().prev())
})

function get_cb_ids(selection) {
    checkboxs_ids = []
    $(selection+':checked').each(function () {
        checkboxs_ids.push(parseInt($(this).attr('data-id')))
    })
    return checkboxs_ids
}


$('#new').click(function () {
    $('#id').val('')
    $('#nombre').val('')
    $('#descripcion').val('')
    $('.module').prop('checked', false)

    verif_inputs('')
    validationInputSelects("form")
    $('#id_div').hide()
    $('#insert').show()
    $('#update').hide()
    $('#form').modal('show')
})


$('#insert').click(function () {
    var permisos = document.querySelectorAll("input[type='checkbox']:checked")
    notvalid = validationInputSelectsWithReturn("form");
    if (notvalid===false) {
        if(permisos.length !=0 ){
            x = get_cb_ids('.module')

            objeto = JSON.stringify({
                'nombre': $('#nombre').val(),
                'descripcion': $('#descripcion').val(),
                'modulos': get_cb_ids('.module')
            })
            ajax_call('rol_insert', {_xsrf: getCookie("_xsrf"), object: objeto}, null, function () {window.location = main_route})
            $('#form').modal('hide')
        }else{
            swal(
                'Error de permisos.',
                'Seleccione al menos un permiso',
                'error'
            )
        }
    }else {
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
        ajax_call_get('rol_update',{
            _xsrf: getCookie("_xsrf"),
            object: obj
        },function(response){
            var self = response;

            $('#id').val(self.id)
            $('#nombre').val(self.nombre)
            $('#descripcion').val(self.descripcion)

            $('.module').prop('checked', false)
            for (i in self.modulos){
                $('.module[data-id="'+self.modulos[i].id+'"]').prop('checked', true)
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


$('#update').click(function() {
    notvalid = validationInputSelectsWithReturn("form");
    if (notvalid === false) {
        objeto = JSON.stringify({
            'id': parseInt($('#id').val()),
            'nombre': $('#nombre').val(),
            'descripcion': $('#descripcion').val(),
            'modulos': get_cb_ids('.module')
        })
        ajax_call('rol_update', {
            _xsrf: getCookie("_xsrf"),
            object: objeto
        }, null, function() {
            window.location = main_route
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


$('.enabled').click(function (e) {
    e.preventDefault()
    cb_delete = this
    b = $(this).prop('checked')
    if(!b){
        cb_title = "¿Está seguro de que desea dar de baja el rol?"
        cb_text = "Los usuarios relacionados, también serán dados de baja."
        cb_type = "warning"
    } else {
        cb_title ="¿Está seguro de que desea dar de alta el rol?"
        cb_text = ""
        cb_type = "info"
    }
    swal({
        title: cb_title,
        text: cb_text,
        type: cb_type,
        showCancelButton: true,
        confirmButtonColor: "#004c99",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    }).then(function () {
        $(cb_delete).prop('checked', !$(cb_delete).is(':checked'))
        if(b) $(cb_delete).parent().prop('title', 'Activo')
        else $(cb_delete).parent().prop('title', 'Inhabilitado')

        objeto =JSON.stringify({
            id: parseInt($(cb_delete).attr('data-id')),
            enabled: $(cb_delete).is(':checked')
        })

        ajax_call('rol_delete', {object: objeto,_xsrf: getCookie("_xsrf")}, null, function () {setTimeout(function(){}, 2000);})
        $('#form').modal('hide')
    })
})

validationKeyup("form")
validationSelectChange("form")