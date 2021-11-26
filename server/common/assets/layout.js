$(document).ready(function () {
    $.extend( true, $.fn.dataTable.defaults, {
        "language": {
            "url": "resources/js/spanish.json"
        },
        dom: '<"pull-left"f><"pull-right"l>tip'
    } );

    let pathname = window.location.pathname; //URL de la página
    let a = document.querySelector("a[href='"+pathname+"']");
    let b = (a.parentNode).parentNode; //tiene LI
    let c = b.previousElementSibling; //tiene a href, elemento anterior a LI
    if (c == null){
        b.style["display"] = "block";
    }else{
        c.classList.add('toggled');
        b.style["display"] = "block";
        a.style["background-color"] = "rgba(0,0,0,.2)";
    }
    fields_keyup()
    inputmask_keyup()
});

function  Salir(logo1) {
    swal({
        title: "¿Desea cerrar sesión?",
        imageUrl: logo1,
        showCancelButton: true,
        confirmButtonColor: "#0B1D50",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        reverseButtons: true,
        cancelButtonText: "Cancelar"
    }).then(function () {
        swal(
              'Gracias por tu trabajo.',
              'Vuelve pronto.',
              'success'
        )
        setTimeout(function () {
            window.location="/logout"
        }, 2000);
    })
}

function  manual(logo1) {
    swal({
        title: "¿Desea ver el manual?",
        imageUrl: logo1,
        showCancelButton: true,
        confirmButtonColor: "#0B1D50",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        reverseButtons: true,
        cancelButtonText: "Cancelar"
    }).then(function () {
        swal(
              'Manual cargado exitosamente.',
              '',
              'success'
            )
        setTimeout(function () {
            window.location="/manual"
        }, 2000);
    })
}

function formatDate(valor) {
    var res = ''
    if (!['', null].includes(valor)) {
        var partd = valor.split("/")
        //console.log(partd)

        if (parseInt(partd[1]) < 10) vlm = '0' + partd[1]
        else  vlm = partd[1]

        if (parseInt(partd[0]) < 10) vld = '0' + partd[0]
        else  vld = partd[0]

        res = vld + '/' + vlm + '/' + partd[2]
    }

    return res
}

function str_to_date(cadena) {
    var partd = cadena.split("/");
    var d = new Date(partd[1]+'/'+partd[0]+'/'+partd[2]);

    return d;
}

$('#dtini').calendar({
    width: 300,
    height: 320,
    data: null,
    weekArray: ['D', 'L', 'M', 'X', 'J', 'V', 'S'],
    monthArray: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octobre', 'Noviembre', 'Diciembre'],
    onSelected: function (view, date, data) {
        $('#fechai').val(date.getDate()+'/'+(date.getMonth() + 1)+'/'+date.getFullYear())
        $('#fechai').parent().addClass('focused');

        if ($('#fechai').val().length < 10) $('#fechai').val(formatDate($('#fechai').val()));
        if ($('#fechaf').val().length < 10) $('#fechaf').val(formatDate($('#fechaf').val()));

        if (str_to_date($('#fechai').val()) > str_to_date($('#fechaf').val())) {
            $('#fechaf').val($('#fechai').val());
            $('#dtfin').calendar('setDate', str_to_date($('#fechai').val()));
            $('#fechaf').parent().addClass('focused');
        }
    }
});

$('#dtfin').calendar({
    width: 300,
    height: 320,
    data: null,
    weekArray: ['D', 'L', 'M', 'X', 'J', 'V', 'S'],
    monthArray: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octobre', 'Noviembre', 'Diciembre'],
    onSelected: function (view, date, data) {
        $('#fechaf').val(date.getDate()+'/'+(date.getMonth() + 1)+'/'+date.getFullYear())
        $('#fechaf').parent().addClass('focused')

        if ($('#fechai').val().length < 10) $('#fechai').val(formatDate($('#fechai').val()));
        if ($('#fechaf').val().length < 10) $('#fechaf').val(formatDate($('#fechaf').val()));

        if (str_to_date($('#fechaf').val()) < str_to_date($('#fechai').val())) {
            $('#fechaf').val($('#fechai').val());
            $('#dtfin').calendar('setDate', str_to_date($('#fechai').val()));
            $('#fechaf').parent().addClass('focused');
        }
    }
});

$('.datei').bootstrapMaterialDatePicker({
    format: 'DD/MM/YYYY',
    clearButton: false,
    weekStart: 1,
    locale: 'es',
    time: false
}).on('change', function (e, date) {
    $(this).parent().addClass('focused');
    $('#fechaf').bootstrapMaterialDatePicker('setMinDate', date);

    if ($(this).val().length < 10) $(this).val(formatDate($(this).val()));
    if ($('#fechaf').val().length < 10) $('#fechaf').val(formatDate($('#fechaf').val()));

    if (str_to_date($(this).val()) > str_to_date($('#fechaf').val())) $('#fechaf').val($(this).val());
});

$('.datef').bootstrapMaterialDatePicker({
    format: 'DD/MM/YYYY',
    clearButton: false,
    weekStart: 1,
    locale: 'es',
    time: false
}).on('change', function (e, date) {
    $(this).parent().addClass('focused');
    $(this).bootstrapMaterialDatePicker('setMinDate', $('#fechai').val());

    if ($('#fechai').val().length < 10) $('#fechai').val(formatDate($('#fechai').val()));
    if ($(this).val().length < 10) $(this).val(formatDate($(this).val()));

    if (str_to_date($(this).val()) < str_to_date($('#fechai').val())) $(this).val($('#fechai').val());
});

$('.dateiboleta').bootstrapMaterialDatePicker({
    format: 'DD/MM/YYYY',
    clearButton: false,
    weekStart: 1,
    locale: 'es',
    time: false
}).on('change', function (e, date) {
    $(this).parent().addClass('focused');
    $('#fechafboleta').bootstrapMaterialDatePicker('setMinDate', date);

    if ($(this).val().length < 10) $(this).val(formatDate($(this).val()));
    if ($('#fechafboleta').val().length < 10) $('#fechafboleta').val(formatDate($('#fechafboleta').val()));

    if (str_to_date($(this).val()) > str_to_date($('#fechafboleta').val())) $('#fechafboleta').val($(this).val());
});

$('.datefboleta').bootstrapMaterialDatePicker({
    format: 'DD/MM/YYYY',
    clearButton: false,
    weekStart: 1,
    locale: 'es',
    time: false
}).on('change', function (e, date) {
    $(this).parent().addClass('focused');
    $(this).bootstrapMaterialDatePicker('setMinDate', $('#fechaiboleta').val());

    if ($('#fechaiboleta').val().length < 10) $('#fechaiboleta').val(formatDate($('#fechaiboleta').val()));
    if ($(this).val().length < 10) $(this).val(formatDate($(this).val()));

    if (str_to_date($(this).val()) < str_to_date($('#fechaiboleta').val())) $(this).val($('#fechaiboleta').val());
});
