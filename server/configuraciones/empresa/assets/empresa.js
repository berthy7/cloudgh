main_route = '/empresa'

$(document).ready(function () {
    $('#data_table').DataTable();
});

$(document).ajaxStart(function () { });

$(document).ajaxStop(function () {
    $.Toast.hideToast();
});


$('#new').click(function () {
    $('#nombre').val('')
    $('#foto1').fileinput('clear');
    $('#foto2').fileinput('clear');
    $('#foto3').fileinput('clear');
    $('.nfoto').hide()

    verif_inputs('')
    $('#id_div').hide()
    $('#insert').show()
    $('#update').hide()
    validationInputSelects("form")
    $('#form').modal('show')
})

$('#insert').on('click',function (e) {
      e.preventDefault();
    var data = new FormData($('#form_submit')[0]);
    notvalid = validationInputSelectsWithReturn("form");
    if (notvalid===false) {
        objeto = JSON.stringify({
            'nombre': $('#nombre').val()
        })
        ruta = "empresa_insert";
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
        ajax_call_get('empresa_update', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            $('#id').val(self.id)
            $('#nombre').val(self.nombre)
            if (self.foto1 != "None" && self.foto1 != "") {
                document.getElementById("imagen_show_img").src = self.foto1;
            } else {
                document.getElementById("imagen_show_img").src = "/resources/images/sinImagen.jpg";
            }
            if (self.foto2 != "None" && self.foto2 != "") {
                document.getElementById("imagen_show_img2").src = self.foto2;
            } else {
                document.getElementById("imagen_show_img2").src = "/resources/images/sinImagen.jpg";
            }
            if (self.foto3 != "None" && self.foto3 != "") {
                document.getElementById("imagen_show_img3").src = self.foto3;
            } else {
                document.getElementById("imagen_show_img3").src = "/resources/images/sinImagen.jpg";
            }


            $('#foto1').fileinput('clear');
            $('#foto2').fileinput('clear');
            $('#foto3').fileinput('clear');
            $('.nfoto').show()

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


$('#update').on('click',function (e) {
      e.preventDefault();
     var data = new FormData($('#form_submit')[0]);
    notvalid = validationInputSelectsWithReturn("form");
    if (notvalid===false) {

        objeto = JSON.stringify({
             'id': $('#id').val(),
             'nombre': $('#nombre').val()
        })
        ruta = "empresa_update";
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
    } else {
        swal(
            'Error de datos.',
             notvalid,
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
        ajax_call('empresa_delete', {
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

validationKeyup("form");
validationSelectChange("form");
