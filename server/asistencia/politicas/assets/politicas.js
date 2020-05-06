main_route = '/politicas'

$(document).ready(function () { });

$(document).ajaxStart(function () { });

$(document).ajaxStop(function () {
    $.Toast.hideToast();
});



$('.show-tick').selectpicker()
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


function attach_edit() {
    $('.edit').click(function () {
        console.log("jsadf")
        obj = JSON.stringify({
            'id': parseInt(JSON.parse($(this).attr('data-json')))
        })

        ajax_call_get('politicas_update', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            console.log(self)
            $('#id').val(self.id)
            $('#nombre').val(self.empresa.nombre)
            $('#toleranciadia').val(self.toleranciadia)
            $('#toleranciames').val(self.toleranciames)

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
            'toleranciadia': $('#toleranciadia').val(),
            'toleranciames': $('#toleranciames').val()
        })
        ajax_call('politicas_update', {
            object: objeto,
            _xsrf: getCookie("_xsrf")
        }, null, function () {
            setTimeout(function () {
                window.location = main_route
            }, 2000);
        })
        $('#form').modal('hide')
    } else {
        swal('Error de datos.',
            'Hay campos vacíos por favor verifique sus datos.',
            'error')
    }
})
reload_form()
