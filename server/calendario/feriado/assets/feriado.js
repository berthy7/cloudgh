main_route = "/feriado"


$(".hr").inputmask("h:s",{ "placeholder": "__/__" });

$('.date').bootstrapMaterialDatePicker({
    format: 'DD/MM/YYYY',
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

document.getElementById("primero").click();


    $('#primero').click(function () {
        $('#body-cont').css("display", "block")
        $('#body-elfec').css("display", "none")
    })

    $('#segundo').click(function () {
        $('#body-cont').css("display", "none")
        $('#body-elfec').css("display", "block")
    })

    $( "#fkpais" ).change(function() {
      $("#fkdepartamento").val('').selectpicker('refresh')
      $("#fkciudad").val('').selectpicker('refresh')
      $("#fksucursal").val('').selectpicker('refresh')
    });

    $( "#fkdepartamento" ).change(function() {
      $("#fkpais").val('').selectpicker('refresh')
      $("#fkciudad").val('').selectpicker('refresh')
      $("#fksucursal").val('').selectpicker('refresh')
    });

    $( "#fkciudad" ).change(function() {
      $("#fkpais").val('').selectpicker('refresh')
      $("#fkdepartamento").val('').selectpicker('refresh')
      $("#fksucursal").val('').selectpicker('refresh')
    });

    $( "#fksucursal" ).change(function() {
      $("#fkpais").val('').selectpicker('refresh')
      $("#fkdepartamento").val('').selectpicker('refresh')
      $("#fkciudad").val('').selectpicker('refresh')
    });


$('#new').click(function () {
     $('#id_div').hide()

     $('#nombre').val('')
     $('#fkpais').val('')
     $('#fkpais').selectpicker('refresh')

     $('#fkdepartamento').val('')
     $('#fkdepartamento').selectpicker('refresh')
     $('#fkciudad').val('')
     $('#fkciudad').selectpicker('refresh')
     $('#fksucursal').val('')
     $('#fksucursal').selectpicker('refresh')

     $('#ciclico').prop('checked', false)
     $('#fijo').prop('checked', true)
     $('#relativo').prop('checked', false)
     verif_inputs('')
     $('#insert').show()
     $('#delete').hide()
     $('#update').hide()
     validationInputSelects("form");
     $('#form').modal('show')
     $('#fecha').val('')
     $('#fecha').attr("disabled", false)

})

$('#insert').click(function () {
    notvalid = validationInputSelectsWithReturn("form");
    if (notvalid===false) {
        objeto = JSON.stringify({
            'nombre': $('#nombre').val(),
            'fecha': $('#fecha').val(),
            'ciclico': $('#ciclico').is(':checked'),
            'fijo': $('#fijo').is(':checked'),
            'relativo': $('#relativo').is(':checked'),
            'fkpais': parseInt($('#fkpais').val()),
            'fkdepartamento': parseInt($('#fkdepartamento').val()),
            'fkciudad': parseInt($('#fkciudad').val()),
            'fksucursal': parseInt($('#fksucursal').val())

        })
        ajax_call('feriado_insert', {
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

$('#update').click(function () {
    notvalid = validationInputSelectsWithReturn("form");
    if (notvalid===false) {
        objeto = JSON.stringify({
            'id': $('#id').val(),
            'nombre': $('#nombre').val(),
            'fecha': $('#fecha').val(),
            'ciclico': $('#ciclico').is(':checked'),
            'fijo': $('#fijo').is(':checked'),
            'relativo': $('#relativo').is(':checked'),
            'fkpais': parseInt($('#fkpais').val()),
            'fkdepartamento': parseInt($('#fkdepartamento').val()),
            'fkciudad': parseInt($('#fkciudad').val()),
            'fksucursal': parseInt($('#fksucursal').val())

        })
        ajax_call('feriado_update', {
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
$('#delete').click(function () {

    objeto = JSON.stringify({
        'id': $('#id').val()

    })
    ajax_call('feriado_delete', {
        object: objeto,
            _xsrf: getCookie("_xsrf")
        }, null, function () {
            setTimeout(function () {
            window.location = main_route
        }, 2000);
    })
    $('#form').modal('hide')

})

$('.delete_tabla').click(function () {
    id = parseInt(JSON.parse($(this).attr('data-json')))
    enabled = false
    swal({
        title: "¿Desea dar de baja el feriado?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#1565c0",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    }).then(function () {
        ajax_call('feriado_delete_tabla', {
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


function attach_edit() {

    $('.edit_tabla').click(function () {
        obj = JSON.stringify({
            'id': parseInt(JSON.parse($(this).attr('data-json')))
        })

        ajax_call_get('feriado_update', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var event = response;
            console.log(event)
            $('#id').val(event.id)
            $('#nombre').val(event.nombre)
            $('#fecha').val(event.fecha)

            if(event.ciclico){
                $('#ciclico').prop('checked', true)
            }

            if(event.fijo){
                $('#fijo').prop('checked', true)
            }

            if(event.relativo){
                $('#relativo').prop('checked', true)
            }


            $('#fkpais').val(event.fkpais)
            $('#fkpais').selectpicker('refresh')

            $('#fkdepartamento').val(event.fkdepartamento)
            $('#fkdepartamento').selectpicker('refresh')
            $('#fkciudad').val(event.fkciudad)
            $('#fkciudad').selectpicker('refresh')
            $('#fksucursal').val(event.fksucursal)
            $('#fksucursal').selectpicker('refresh')

            $('#id_div').hide()
            $('#insert').hide()
            $('#delete').show()
            $('#update').show()
            $('#form').modal('show')
        })
    })

}
attach_edit()

reload_form()

validationKeyup("form");
validationSelectChange("form");