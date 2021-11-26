main_route = '/pais'

$(document).ready(function () {
    $('#data_table').DataTable();
//     if ("geolocation" in navigator){ //check geolocation available
//     //try to get user current location using getCurrentPosition() method
//     navigator.geolocation.getCurrentPosition(function(position){
//             console.log("Found your location nLat : "+position.coords.latitude+" nLang :"+ position.coords.longitude);
//         });
// }else{
//     console.log("Browser doesn't support geolocation!");
// }

});

$(document).ajaxStart(function () {});

$(document).ajaxStop(function () {
    $.Toast.hideToast();
});





$('#new').click(function () {
    $('#nombre').val('')


    // var latitud = -16.2901535;
    // var longitud = -63.5886536;
    // localStorage.setItem('latitud',latitud);
    // localStorage.setItem('longitud',longitud);
    // cargar_mapa()
    


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
            // 'latitud':localStorage.getItem("latitud"),
            // 'longitud':localStorage.getItem("longitud")

        })
        ajax_call('pais_insert', {
            object: objeto,
            _xsrf: getCookie("_xsrf")
        }, null, function () {
            setTimeout(function () {
                window.location = main_route
            }, 2000);
        })
        $("#iframe").attr("src", "configuraciones/pais/views/mapa.html")
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
        ajax_call_get('pais_update', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            $('#id').val(self.id)
            $('#nombre').val(self.nombre)
            // localStorage.setItem('latitud',self.latitud)
            // localStorage.setItem('longitud',self.longitud)
            //
            // funcion_actualizar()

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
            'nombre': $('#nombre').val(),
            // 'latitud':localStorage.getItem("latitud"),
            // 'longitud':localStorage.getItem("longitud")
        })
        ajax_call('pais_update', {
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


$('.delete').click(function () {
    id = parseInt(JSON.parse($(this).attr('data-json')))
    enabled = false
    swal({
        title: "¿Desea dar de baja los datos del país?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#1565c0",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    }).then(function () {
        ajax_call('pais_delete', {
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