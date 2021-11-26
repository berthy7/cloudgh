main_route = '/persona'

var gb_id = 0;
var gb_msg = '';
var gb_ret = 0;
var datos_elem = [];

$(document).ready(function () {
    $('#data_table').DataTable();
});

$('#sexo').selectpicker({
    size: 7,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar opción',
    title: 'Seleccione un género'
})

$('#fkpais').selectpicker({
    size: 7,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar país',
    title: 'Seleccione un país'
})

$('#fkdepartamento').selectpicker({
    size: 7,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar departamento',
    title: 'Seleccione un departamento'
})

$('#fkciudad').selectpicker({
    size: 7,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar ciudad',
    title: 'Seleccione una ciudad'
})

$('#fksucursal').selectpicker({
    size: 7,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar sucursal',
    title: 'Seleccione una sucursal'
})

$('#fkoficina').selectpicker({
    size: 7,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar oficina',
    title: 'Seleccione una oficina'
})

$('#fkgerencia').selectpicker({
    size: 7,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar área de trabajo',
    title: 'Seleccione un área de trabajo'
})

$('#fkcargo').selectpicker({
    size: 7,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar cargo',
    title: 'Seleccione un cargo'
})

$('#fkcentro').selectpicker({
    size: 7,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar centro de costo',
    title: 'Seleccione un centro de costo'
})

$('#tipotrabajador').selectpicker({
    size: 7,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar tipo',
    title: 'Seleccione un tipo'
})

$('#banco').selectpicker({
    size: 7,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar banco',
    title: 'Seleccione un banco'
})

$('#hijos').selectpicker({
    size: 7,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar opción',
    title: 'Seleccione una opción'
})

$('#estadocivil').selectpicker({
    size: 7,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar opción',
    title: 'Seleccione un estado civil'
})

$('#domiciliocasa').selectpicker({
    size: 7,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar opción',
    title: 'Seleccione un domicilio'
})

$('#niveleducativo').selectpicker({
    size: 7,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar opción',
    title: 'Seleccione un nivel educativo'
})

$('#tipocentroestudio').selectpicker({
    size: 7,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar tipo',
    title: 'Seleccione un tipo de centro educativo'
})

$('#condicionactual').selectpicker({
    size: 7,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar opción',
    title: 'Seleccione una condición actual'
})

$('#situacionp').selectpicker({
    size: 7,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar opción',
    title: 'Seleccione una opción'
})

$('#situacionm').selectpicker({
    size: 7,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar opción',
    title: 'Seleccione una opción'
})

$('#sexoc').selectpicker({
    size: 7,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar opción',
    title: 'Seleccione un género'
})

$('#tipocont').selectpicker({
    size: 7,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar tipo',
    title: 'Seleccione un Tipo de Contrato'
})


$('#fkpais').change(function () {
    obj = JSON.stringify({
        'idpais': parseInt(JSON.parse($('#fkpais').val())),
        '_xsrf': getCookie("_xsrf")
    })
    ruta = "listar_x_pais";

    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: false
    }).done(function (response) {
        response = JSON.parse(response)
        $('#fkdepartamento').html('');
        var select = document.getElementById("fkdepartamento")

        for (var i = 0; i < Object.keys(response.response).length; i++) {
            var option = document.createElement("OPTION");
            option.innerHTML = response['response'][i]['nombre'];
            option.value = response['response'][i]['id'];
            select.appendChild(option);
        }

        document.getElementById("fkdepartamento").selectedIndex = "-1"
        $('#fkdepartamento').selectpicker('refresh');

        $('#fkciudad').html('');
        $('#fkciudad').selectpicker('refresh');

        $('#fksucursal').html('');
        $('#fksucursal').selectpicker('refresh');

        $('#fkoficina').html('');
        $('#fkoficina').selectpicker('refresh');
    })
});

$('#fkdepartamento').change(function () {
    obj = JSON.stringify({
        'iddepartamento': parseInt(JSON.parse($('#fkdepartamento').val())),
        '_xsrf': getCookie("_xsrf")
    })
    ruta = "listar_x_departamento";

    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: false
    }).done(function (response) {
        response = JSON.parse(response)
        $('#fkciudad').html('');
        var select = document.getElementById("fkciudad")

        for (var i = 0; i < Object.keys(response.response).length; i++) {
            var option = document.createElement("OPTION");
            option.innerHTML = response['response'][i]['nombre'];
            option.value = response['response'][i]['id'];
            select.appendChild(option);
        }
        document.getElementById("fkciudad").selectedIndex = "-1"
        $('#fkciudad').selectpicker('refresh');

        $('#fksucursal').html('');
        $('#fksucursal').selectpicker('refresh');

        $('#fkoficina').html('');
        $('#fkoficina').selectpicker('refresh');
    })
});

$('#fkciudad').change(function () {
    obj = JSON.stringify({
        'idciudad': parseInt(JSON.parse($('#fkciudad').val())),
        '_xsrf': getCookie("_xsrf")
    })
    ruta = "listar_x_ciudad";

    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: false
    }).done(function (response) {
        response = JSON.parse(response)
        $('#fksucursal').html('');
        var select = document.getElementById("fksucursal")

        for (var i = 0; i < Object.keys(response.response).length; i++) {
            var option = document.createElement("OPTION");
            option.innerHTML = response['response'][i]['nombre'];
            option.value = response['response'][i]['id'];
            select.appendChild(option);
        }
        document.getElementById("fksucursal").selectedIndex = "-1"
        $('#fksucursal').selectpicker('refresh');

        $('#fkoficina').html('');
        $('#fkoficina').selectpicker('refresh');
    })
});

$('#fksucursal').change(function () {
    obj = JSON.stringify({
        'idsucursal': parseInt(JSON.parse($('#fksucursal').val())),
        '_xsrf': getCookie("_xsrf")
    })
    ruta = "listar_x_sucursal";

    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: false
    }).done(function (response) {
        response = JSON.parse(response)
        $('#fkoficina').html('');
        var select = document.getElementById("fkoficina")

        for (var i = 0; i < Object.keys(response.response).length; i++) {
            var option = document.createElement("OPTION");
            option.innerHTML = response['response'][i]['nombre'];
            option.value = response['response'][i]['id'];
            select.appendChild(option);
        }
        document.getElementById("fkoficina").selectedIndex = "-1"
        $('#fkoficina').selectpicker('refresh');
    })
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
    maxDate: new Date(),
    time: false
}).on('change', function (e, date) {
    $(this).parent().addClass('focused');
    $('#f_date').bootstrapMaterialDatePicker('setMinDate', date);
});


function item_is_empty(items){
    //console.log('MTDH into')
    //console.log(items)
    for (ic = 0; ic < items.length; ic++) {
    //console.log(items[ic])
        if(items[ic] == ''){
            //console.log('mtdh T')
            return true;
        }
    }
    //console.log('mthd F')
    return false;
}


function get_empleado() {
    data = [];
    var object_inputs = $('.empleado');

     console.log(object_inputs[0].value);
    console.log(object_inputs[1].value);
    console.log(object_inputs[2].value);
    console.log(object_inputs[4].value);
    console.log(object_inputs[6].value);
    console.log(object_inputs[8].value);
    console.log(object_inputs[10].value);
    console.log(object_inputs[12].value);
    console.log(object_inputs[14].value);
    console.log(object_inputs[16].value);
    console.log(object_inputs[28].value);


    h0 = object_inputs[0].value;
    h1 = object_inputs[1].value;
    h4 = object_inputs[2].value;
    h5 = object_inputs[4].value;
    h6 = object_inputs[6].value;
    h7 = object_inputs[8].value;
    h8 = object_inputs[10].value;
    h9 = object_inputs[12].value;
    h10 = object_inputs[14].value;
    h11 = object_inputs[16].value;
    h12 = object_inputs[28].value;

    //items = [h1, h2, h3, h4, h5, h6, h7, h8, h9, h10];
    items = [h4];
    if (item_is_empty(items)) {
        gb_msg+= 'datos administrativos';
        return;
    }

        data.push((function get_items(h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10) {
            if (h0 ==''){
                return {
                    'email': h1,
                    'codigo':h2,
                    'fkpais':h3,
                    'fkdepartamento':h4,
                    'fkciudad':h5,
                    'fksucursal':h6,
                    'fkoficina':h7,
                    'fkgerencia':h8,
                    'fkcargo':h9,
                    'fkcentro':h10
                }

            }else{
                return {
                    'id':h0,
                    'email': h1,
                    'codigo':h2,
                    'fkpais':h3,
                    'fkdepartamento':h4,
                    'fkciudad':h5,
                    'fksucursal':h6,
                    'fkoficina':h7,
                    'fkgerencia':h8,
                    'fkcargo':h9,
                    'fkcentro':h10
                }
            }

        })(
            h0,
            h1,
            h2,
            h3,
            h4,
            h5,
            h6,
            h7,
            h8,
            h9,
            h10
        ))

    return data
}

function get_contrato() {
    data = [];
    object_inputs = $('.contrato');
    //console.log(object_inputs)

    h0 = object_inputs[0].value;
    h1 = object_inputs[1].value;
    h2 = object_inputs[3].value;
    h3 = object_inputs[4].value;
    h4 = object_inputs[5].value;
    h5 = object_inputs[6].value;
    h6 = object_inputs[7].value;
    h7 = object_inputs[8].value;
    h8 = object_inputs[9].value;

    items = [h1, h2, h3, h4];

    if (item_is_empty(items)) {
        if(gb_msg != '') gb_msg+= ' contrato';
        else gb_msg+= 'contrato';
        return;
    }
    if(h0 == ''){
        data.push((function get_items(h1, h2, h3, h4, h5, h6, h7, h8) {
            return {
                'nroContrato': h1,
                'tipo':h2,
                'sueldo':h3,
                'fechaIngreso':h4,
                'fechaFin':h5,
                'fechaForzado':h6,
                'descripcion':h7,
                'enabled': h8
            }
        })(
            object_inputs[1].value,
            object_inputs[3].value,
            object_inputs[4].value,
            !['None', null, ""].includes(object_inputs[5].value)? object_inputs[5].value+' 00:00:00': null,
            !['None', null, ""].includes(object_inputs[6].value)? object_inputs[6].value+' 00:00:00': null,
            !['None', null, ""].includes(object_inputs[7].value)? object_inputs[7].value+' 00:00:00': null,
            object_inputs[8].value,
            object_inputs[9].value === 'true'? true: false
        ))
    }else{
        data.push((function get_items(h0, h1, h2, h3, h4, h5, h6, h7, h8) {
            return {
                'id': h0,
                'nroContrato': h1,
                'tipo':h2,
                'sueldo':h3,
                'fechaIngreso':h4,
                'fechaFin':h5,
                'fechaForzado':h6,
                'descripcion':h7,
                'enabled': h8
            }
        })(
            object_inputs[0].value,
            object_inputs[1].value,
            object_inputs[3].value,
            object_inputs[4].value,
            !['None', null, ""].includes(object_inputs[5].value)? object_inputs[5].value+' 00:00:00': null,
            !['None', null, ""].includes(object_inputs[6].value)? object_inputs[6].value+' 00:00:00': null,
            !['None', null, ""].includes(object_inputs[7].value)? object_inputs[7].value+' 00:00:00': null,
            object_inputs[8].value,
            object_inputs[9].value === 'true'? true: false
        ))
    }

    return data
}

function get_administrativo() {
    data = [];
    object_inputs = $('.administrativo');
    //console.log(object_inputs)

    h0 = object_inputs[0].value;
    h1 = object_inputs[1].value;
    h2 = object_inputs[2].value;
    h3 = object_inputs[3].value;
    h4 = object_inputs[5].value;
    h5 = object_inputs[6].value;
    h6 = object_inputs[8].value;
    h7 = object_inputs[9].value;
    h8 = object_inputs[10].value;
    h9 = object_inputs[11].value;
    h10 = object_inputs[12].value;
    h11 = object_inputs[13].value;
    h12 = object_inputs[15].value;
    h13 = object_inputs[17].value;
    h14 = object_inputs[18].value;
    h15 = object_inputs[19].value;
    h16 = object_inputs[20].value;
    h17 = object_inputs[21].value;
    h18 = object_inputs[22].value;
    h19 = object_inputs[23].value;
    h20 = object_inputs[24].value;
    h21 = object_inputs[25].value;
    h22 = object_inputs[26].value;
    h23 = object_inputs[27].value;
    h24 = object_inputs[29].value;

    items = [h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14, h15, h16, h17, h18, h19, h20, h21, h22, h23, h24];

    if (item_is_empty(items)) {
        if(gb_msg != '') gb_msg+= ' administrativo';
        else gb_msg+= 'administrativo';
        return;
    }
    if(h0 == ''){
        data.push((function get_items(h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14, h15, h16, h17, h18, h19, h20, h21, h22, h23, h24) {
            return {
                'nroAsegurado': h1,
                'cajaSalud': h2,
                'afp': h3,
                'banco': h4,
                'nroCuenta': h5,
                'tipoTrabajador': h6,
                'libretaMilitar': h7,
                'brevete': h8,
                'grupoSanguineo': h9,
                'telefonoFijo': h10,
                'telefonoCelular': h11,
                'hijos': h12,
                'estadoCivil': h13,
                'nacimientoPais': h14,
                'nacimientoDepartamento': h15,
                'nacimientoProvincia': h16,
                'nacimientoDistrito': h17,
                'nacimientoDomicilio': h18,
                'domicilioPais': h19,
                'domicilioDepartamento': h20,
                'domicilioProvincia': h21,
                'domicilioDistrito': h22,
                'domiciliodireccion': h23,
                'domicilioCasa': h24
            }
        })(
            object_inputs[1].value,
            object_inputs[2].value,
            object_inputs[3].value,
            object_inputs[5].value,
            object_inputs[6].value,
            object_inputs[8].value,
            object_inputs[9].value,
            object_inputs[10].value,
            object_inputs[11].value,
            object_inputs[12].value,
            object_inputs[13].value,
            object_inputs[15].value,
            object_inputs[17].value,
            object_inputs[18].value,
            object_inputs[19].value,
            object_inputs[20].value,
            object_inputs[21].value,
            object_inputs[22].value,
            object_inputs[23].value,
            object_inputs[24].value,
            object_inputs[25].value,
            object_inputs[26].value,
            object_inputs[27].value,
            object_inputs[29].value
        ))
    }else{
        data.push((function get_items(h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14, h15, h16, h17, h18, h19, h20, h21, h22, h23, h24) {
            return {
                'id': h0,
                'nroAsegurado': h1,
                'cajaSalud': h2,
                'afp': h3,
                'banco': h4,
                'nroCuenta': h5,
                'tipoTrabajador': h6,
                'libretaMilitar': h7,
                'brevete': h8,
                'grupoSanguineo': h9,
                'telefonoFijo': h10,
                'telefonoCelular': h11,
                'hijos': h12,
                'estadoCivil': h13,
                'nacimientoPais': h14,
                'nacimientoDepartamento': h15,
                'nacimientoProvincia': h16,
                'nacimientoDistrito': h17,
                'nacimientoDomicilio': h18,
                'domicilioPais': h19,
                'domicilioDepartamento': h20,
                'domicilioProvincia': h21,
                'domicilioDistrito': h22,
                'domiciliodireccion': h23,
                'domicilioCasa': h24
            }
        })(
            object_inputs[0].value,
            object_inputs[1].value,
            object_inputs[2].value,
            object_inputs[3].value,
            object_inputs[5].value,
            object_inputs[6].value,
            object_inputs[8].value,
            object_inputs[9].value,
            object_inputs[10].value,
            object_inputs[11].value,
            object_inputs[12].value,
            object_inputs[13].value,
            object_inputs[15].value,
            object_inputs[17].value,
            object_inputs[18].value,
            object_inputs[19].value,
            object_inputs[20].value,
            object_inputs[21].value,
            object_inputs[22].value,
            object_inputs[23].value,
            object_inputs[24].value,
            object_inputs[25].value,
            object_inputs[26].value,
            object_inputs[27].value,
            object_inputs[29].value
        ))
    }

    return data
}

function get_educacion() {
    data = [];
    object_inputs = $('.educacion');

    h0 = object_inputs[0].value;
    h1 = object_inputs[2].value;
    h2 = object_inputs[4].value;
    h3 = object_inputs[6].value;
    h4 = object_inputs[7].value;
    h5 = object_inputs[8].value;
    h6 = object_inputs[9].value;

    items = [h1, h2, h3, h4, h5, h6];

    if (item_is_empty(items)) {
        if(gb_msg != '') gb_msg+= ' educación';
        else gb_msg+= 'educación';
        return;
    }
    if(h0 == ''){
        data.push((function get_items(h1, h2, h3, h4, h5, h6) {
            return {
                'nivelEducativo': h1,
                'tipoCentroEstudio': h2,
                'condicionActual': h3,
                'nombreCentroEstudio': h4,
                'profesion': h5,
                'fechaTitulo': h6
            }
        })(
            object_inputs[2].value,
            object_inputs[4].value,
            object_inputs[6].value,
            object_inputs[7].value,
            object_inputs[8].value,
            object_inputs[9].value
        ))
    }else{
        data.push((function get_items(h0, h1, h2, h3, h4, h5) {
            return {
                'id': h0,
                'nivelEducativo': h1,
                'tipoCentroEstudio': h2,
                'condicionActual': h3,
                'nombreCentroEstudio': h4,
                'profesion': h5,
                'fechaTitulo': h6
            }
        })(
            object_inputs[0].value,
            object_inputs[2].value,
            object_inputs[4].value,
            object_inputs[6].value,
            object_inputs[7].value,
            object_inputs[8].value,
            object_inputs[9].value
        ))
    }

    return data
}

function get_capacitacion() {
    data = [];
    object_inputs = $('.capacitacion');

    for (k = 0; k < object_inputs.length; k += 5) {
        h0 = object_inputs[k].value;
        h1 = object_inputs[k+1].value;
        h2 = object_inputs[k+2].value;
        h3 = object_inputs[k+3].value;
        h4 = object_inputs[k+4].value;

        items = [h1, h2, h3, h4];

        if (item_is_empty(items)) {
            if(gb_msg != '') gb_msg+= ' capacitación';
            else gb_msg+= 'capacitación';
            return;
        }
        if((object_inputs[k].id).includes('nw')){
            data.push((function get_items(h1, h2, h3, h4) {
                return {
                    'detalle':h1,
                    'documento':h2,
                    'fechaInicio': h3,
                    'fechaFin': h4
                }
            })(
                object_inputs[k+1].value,
                object_inputs[k+2].value,
                object_inputs[k+3].value,
                object_inputs[k+4].value
            ))
        }else{
            data.push((function get_items(h0, h1, h2, h3, h4) {
                return {
                    'id': h0,
                    'detalle':h1,
                    'documento':h2,
                    'fechaInicio': h3,
                    'fechaFin': h4
                }
            })(
                object_inputs[k].value,
                object_inputs[k+1].value,
                object_inputs[k+2].value,
                object_inputs[k+3].value,
                object_inputs[k+4].value
            ))
        }
    }

    return data
}

function get_estudio() {
    data = [];
    object_inputs = $('.estudio');
    //console.log(object_inputs)

    for (m = 0; m < object_inputs.length; m += 4) {
        //console.log(m)
        h0 = object_inputs[m].value;
        h1 = object_inputs[m+1].value;
        h2 = object_inputs[m+2].value;
        h3 = object_inputs[m+3].value;

        items = [h1, h2, h3];

        if (item_is_empty(items)) {
            if(gb_msg != '') gb_msg+= ' estudio';
            else gb_msg+= 'estudio';
            return;
        }
        if((object_inputs[m].id).includes('nw')){
            data.push((function get_items(h1, h2, h3) {
                return {
                    'detalle':h1,
                    'gestion':h2,
                    'tipo': h3
                }
            })(
                object_inputs[m+1].value,
                object_inputs[m+2].value,
                object_inputs[m+3].value
            ))
        }else{
            data.push((function get_items(h0, h1, h2, h3) {
                return {
                    'id': h0,
                    'detalle':h1,
                    'gestion':h2,
                    'tipo': h3
                }
            })(
                object_inputs[m].value,
                object_inputs[m+1].value,
                object_inputs[m+2].value,
                object_inputs[m+3].value
            ))
        }
    }

    return data
}

function get_beca() {
    data = [];
    object_inputs = $('.beca');
    //console.log(object_inputs)

    for (n = 0; n < object_inputs.length; n += 6) {
        //console.log(n)
        h0 = object_inputs[n].value;
        h1 = object_inputs[n+1].value;
        h2 = object_inputs[n+2].value;
        h3 = object_inputs[n+3].value;
        h4 = object_inputs[n+4].value;
        h5 = object_inputs[n+5].value;

        items = [h1, h2, h3, h4, h5];

        if (item_is_empty(items)) {
            if(gb_msg != '') gb_msg+= ' beca';
            else gb_msg+= 'beca';
            return;
        }
        if((object_inputs[n].id).includes('nw')){
            data.push((function get_items(h1, h2, h3, h4, h5) {
                return {
                    'documento':h1,
                    'evento':h2,
                    'detalle': h3,
                    'fechaInicio': h4,
                    'fechaFin': h5
                }
            })(
                object_inputs[n+1].value,
                object_inputs[n+2].value,
                object_inputs[n+3].value,
                object_inputs[n+4].value,
                object_inputs[n+5].value
            ))
        }else{
            data.push((function get_items(h0, h1, h2, h3, h4, h5) {
                return {
                    'id': h0,
                    'documento':h1,
                    'evento':h2,
                    'detalle': h3,
                    'fechaInicio': h4,
                    'fechaFin': h5
                }
            })(
                object_inputs[n].value,
                object_inputs[n+1].value,
                object_inputs[n+2].value,
                object_inputs[n+3].value,
                object_inputs[n+4].value,
                object_inputs[n+5].value
            ))
        }
    }

    return data
}

function get_idioma() {
    //console.log('lang into')
    data = [];
    object_inputs = $('.idioma');
    //console.log(object_inputs)

    //console.log('cycle lang')
    for (p = 0; p < object_inputs.length; p += 6) {
        //console.log(p)
        h0 = object_inputs[p].value;
        h1 = object_inputs[p+1].value;
        h2 = object_inputs[p+2].checked;
        h3 = object_inputs[p+3].checked;
        h4 = object_inputs[p+4].checked;
        h5 = object_inputs[p+5].checked;

        items = [h1];

        if (item_is_empty(items)) {
            //console.log('lang empty')
            if(gb_msg != '') gb_msg+= ' idioma';
            else gb_msg+= 'idioma';
            return;
        }
        if((object_inputs[p].id).includes('nw')){
            //console.log('no id lang')
            data.push((function get_items(h1, h2, h3, h4, h5) {
                return {
                    'idioma':h1,
                    'habla':h2,
                    'lee': h3,
                    'escribe': h4,
                    'aprendio': h5
                }
            })(
                object_inputs[p+1].value,
                object_inputs[p+2].checked,
                object_inputs[p+3].checked,
                object_inputs[p+4].checked,
                object_inputs[p+5].checked
            ))
        }else{
            //console.log('id lang')
            data.push((function get_items(h0, h1, h2, h3, h4, h5) {
                return {
                    'id': h0,
                    'idioma':h1,
                    'habla':h2,
                    'lee': h3,
                    'escribe': h4,
                    'aprendio': h5
                }
            })(
                object_inputs[p].value,
                object_inputs[p+1].value,
                object_inputs[p+2].checked,
                object_inputs[p+3].checked,
                object_inputs[p+4].checked,
                object_inputs[p+5].checked
            ))
        }
    }

    //console.log('lang out')
    return data
}

function get_experiencia() {
    data = [];
    object_inputs = $('.experiencia');
    //console.log(object_inputs)

    for (q = 0; q < object_inputs.length; q += 3) {
        //console.log(q)
        h0 = object_inputs[q].value;
        h1 = object_inputs[q+1].value;
        h2 = object_inputs[q+2].value;

        items = [h1, h2];

        if (item_is_empty(items)) {
            if(gb_msg != '') gb_msg+= ' experiencia';
            else gb_msg+= 'experiencia';
            return;
        }
        if((object_inputs[q].id).includes('nw')){
            data.push((function get_items(h1, h2) {
                return {
                    'especialidad':h1,
                    'entidad':h2
                }
            })(
                object_inputs[q+1].value,
                object_inputs[q+2].value
            ))
        }else{
            data.push((function get_items(h0, h1, h2) {
                return {
                    'id': h0,
                    'especialidad':h1,
                    'entidad':h2
                }
            })(
                object_inputs[q].value,
                object_inputs[q+1].value,
                object_inputs[q+2].value
            ))
        }
    }

    return data
}

function get_padres() {
    data = [];
    object_inputs = $('.padres');

    for (j = 0; j < object_inputs.length; j+=7) {
        h0 = object_inputs[j].value;
        h1 = object_inputs[j+1].value;
        h2 = object_inputs[j+2].value;
        h3 = object_inputs[j+3].value;
        h4 = object_inputs[j+5].value;
        h5 = object_inputs[j+6].value;

        items = [h1, h2, h3, h4, h5];

        if (item_is_empty(items)) {
            if(gb_msg != '') gb_msg+= ' padres';
            else gb_msg+= 'padres';
            return;
        }
        if(h0 == ''){
            data.push((function get_items(h1, h2, h3, h4, h5) {
                return {
                    'tipo':h1,
                    'nombreCompleto':h2,
                    'fechanacimiento':h3,
                    'situacion':h4,
                    'telefono':h5
                }
            })(
                object_inputs[j+1].value,
                object_inputs[j+2].value,
                object_inputs[j+3].value,
                object_inputs[j+5].value,
                object_inputs[j+6].value
            ))
        }else{
            data.push((function get_items(h0, h1, h2, h3, h4, h5) {
                return {
                    'id': h0,
                    'tipo':h1,
                    'nombreCompleto':h2,
                    'fechanacimiento':h3,
                    'situacion':h4,
                    'telefono':h5
                }
            })(
                object_inputs[j].value,
                object_inputs[j+1].value,
                object_inputs[j+2].value,
                object_inputs[j+3].value,
                object_inputs[j+5].value,
                object_inputs[j+6].value
            ))
        }
    }

    return data
}

function get_conyuge() {
    data = [];
    object_inputs = $('.conyuge');

    h0 = object_inputs[0].value;
    h1 = object_inputs[1].value;
    h2 = object_inputs[2].value;
    h3 = object_inputs[3].value;
    h4 = object_inputs[5].value;
    h5 = object_inputs[6].value;
    h6 = object_inputs[7].value;
    h7 = object_inputs[8].value;
    h8 = object_inputs[9].value;
    h9 = object_inputs[10].value;
    h10 = object_inputs[11].value;
    h11 = object_inputs[12].value;
    h12 = object_inputs[13].value;
    h13 = object_inputs[14].value;

    items = [h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13];

    if (item_is_empty(items)) {
        if(gb_msg != '') gb_msg+= ' conyuge';
        else gb_msg+= 'conyuge';
        return;
    }
    if(h0 == ''){
        data.push((function get_items(h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13) {
            return {
                'nombreCompleto':h1,
                'fechanacimiento':h2,
                'ci':h3,
                'sexo':h4,
                'pais':h5,
                'departamento':h6,
                'provincia':h7,
                'distrito':h8,
                'domicilio':h9,
                'telefono':h10,
                'instruccion':h11,
                'ocupacion':h12,
                'centroTabajo':h13
            }
        })(
            object_inputs[1].value,
            object_inputs[2].value,
            object_inputs[3].value,
            object_inputs[5].value,
            object_inputs[6].value,
            object_inputs[7].value,
            object_inputs[8].value,
            object_inputs[9].value,
            object_inputs[10].value,
            object_inputs[11].value,
            object_inputs[12].value,
            object_inputs[13].value,
            object_inputs[14].value
        ))
    }else{
        data.push((function get_items(h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13) {
            return {
                'id': h0,
                'nombreCompleto':h1,
                'fechanacimiento':h2,
                'ci':h3,
                'sexo':h4,
                'pais':h5,
                'departamento':h6,
                'provincia':h7,
                'distrito':h8,
                'domicilio':h9,
                'telefono':h10,
                'instruccion':h11,
                'ocupacion':h12,
                'centroTabajo':h13
            }
        })(
            object_inputs[0].value,
            object_inputs[1].value,
            object_inputs[2].value,
            object_inputs[3].value,
            object_inputs[5].value,
            object_inputs[6].value,
            object_inputs[7].value,
            object_inputs[8].value,
            object_inputs[9].value,
            object_inputs[10].value,
            object_inputs[11].value,
            object_inputs[12].value,
            object_inputs[13].value,
            object_inputs[14].value
        ))
    }

    return data
}

function get_hijos() {
    data = [];
    object_inputs = $('.hijo');
    //console.log(object_inputs)

    for (r = 0; r < object_inputs.length; r += 5) {
        //console.log(r)
        h0 = object_inputs[r].value;
        h1 = object_inputs[r+1].value;
        h2 = object_inputs[r+2].value;
        h3 = object_inputs[r+3].value;
        h4 = object_inputs[r+4].value;

        items = [h1, h2, h3, h4];

        if (item_is_empty(items)) {
            if(gb_msg != '') gb_msg+= ' hijos';
            else gb_msg+= 'hijos';
            return;
        }
        if((object_inputs[r].id).includes('nw')){
            data.push((function get_items(h1, h2, h3, h4) {
                return {
                    'nombrecompleto':h1,
                    'direccion':h2,
                    'telefono':h3,
                    'fechanacimiento':h4
                }
            })(
                object_inputs[r+1].value,
                object_inputs[r+2].value,
                object_inputs[r+3].value,
                object_inputs[r+4].value
            ))
        }else{
            data.push((function get_items(h0, h1, h2, h3, h4) {
                return {
                    'id': h0,
                    'nombrecompleto':h1,
                    'direccion':h2,
                    'telefono':h3,
                    'fechanacimiento':h4
                }
            })(
                object_inputs[r].value,
                object_inputs[r+1].value,
                object_inputs[r+2].value,
                object_inputs[r+3].value,
                object_inputs[r+4].value
            ))
        }
    }

    return data
}


function cargar_datos_administrativos(self) {
    var sucursal = self.empleado[0].fksucursal
    var ciudad = self.empleado[0].fkciudad
    var departamento = self.empleado[0].fkdepartamento
    var pais = self.empleado[0].fkpais

    $('#fkpais').val(pais);
    $('#fkpais').selectpicker('refresh');

    obj = JSON.stringify({
        'idpais': parseInt(JSON.parse($('#fkpais').val())),
        '_xsrf': getCookie("_xsrf")
    })
    ruta = "listar_x_pais";

    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: false
    }).done(function (response) {
        response = JSON.parse(response)
        $('#fkdepartamento').html('');
        var select = document.getElementById("fkdepartamento")

        for (var i = 0; i < Object.keys(response.response).length; i++) {
            var option = document.createElement("OPTION");
            option.innerHTML = response['response'][i]['nombre'];
            option.value = response['response'][i]['id'];
            select.appendChild(option);
        }
        $('#fkdepartamento').selectpicker('refresh');

        $('#fkdepartamento').val(departamento);
        $('#fkdepartamento').selectpicker('refresh');
    })

    obj = JSON.stringify({
        'iddepartamento': parseInt(JSON.parse($('#fkdepartamento').val())),
        '_xsrf': getCookie("_xsrf")
    })
    ruta = "listar_x_departamento";

    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: false
    }).done(function (response) {
        response = JSON.parse(response)
        $('#fkciudad').html('');
        var select = document.getElementById("fkciudad")

        for (var i = 0; i < Object.keys(response.response).length; i++) {
            var option = document.createElement("OPTION");
            option.innerHTML = response['response'][i]['nombre'];
            option.value = response['response'][i]['id'];
            select.appendChild(option);
        }
        $('#fkciudad').selectpicker('refresh');

        $('#fkciudad').val(ciudad);
        $('#fkciudad').selectpicker('refresh');
    })

    obj = JSON.stringify({
        'idciudad': parseInt(JSON.parse($('#fkciudad').val())),
        '_xsrf': getCookie("_xsrf")
    })
    ruta = "listar_x_ciudad";

    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: false
    }).done(function (response) {
        response = JSON.parse(response)
        $('#fksucursal').html('');
        var select = document.getElementById("fksucursal")

        for (var i = 0; i < Object.keys(response.response).length; i++) {
            var option = document.createElement("OPTION");
            option.innerHTML = response['response'][i]['nombre'];
            option.value = response['response'][i]['id'];
            select.appendChild(option);
        }
        $('#fksucursal').selectpicker('refresh');

        $('#fksucursal').val(sucursal);
        $('#fksucursal').selectpicker('refresh');
    })

    obj = JSON.stringify({
        'idsucursal': parseInt(JSON.parse($('#fksucursal').val())),
        '_xsrf': getCookie("_xsrf")
    })
    ruta = "listar_x_sucursal";

    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: false
    }).done(function (response) {
        response = JSON.parse(response)
        $('#fkoficina').html('');
        var select = document.getElementById("fkoficina")

        for (var i = 0; i < Object.keys(response.response).length; i++) {
            var option = document.createElement("OPTION");
            option.innerHTML = response['response'][i]['nombre'];
            option.value = response['response'][i]['id'];
            select.appendChild(option);
        }
        $('#fkoficina').selectpicker('refresh');
    })
}

$('#new_capacitacion').click(function () {
    append_input_capacitacion(datos_elem)
})

$('#new_estudio').click(function () {
    append_input_estudio(datos_elem)
})

$('#new_beca').click(function () {
    append_input_beca(datos_elem)
})

$('#new_idioma').click(function () {
    append_input_idioma(datos_elem)
})

$('#new_experiencia').click(function () {
    append_input_experiencia(datos_elem)
})

$('#new_hijo').click(function () {
    append_input_hijo(datos_elem)
})


function append_input_capacitacion(id_in) {
    if(id_in.length === 0){
        gb_id++;
        var_id = 'nw'+gb_id;
        elem = 0;
    }else{
        var_id = id_in[0];
        elem = id_in[0];
    }

    $('#capacitacion_div').append(
        '<div class="row">\
            <div class="col-md-1 hidden">\
                <div class="form-group form-float">\
                    <div class="form-line">\
                        <input id="id'+var_id+'" value="'+elem+'" class="form-control capacitacion readonly">\
                    </div>\
                </div>\
            </div>\
            <div class="col-sm-3">\
                <div class="form-group form-float">\
                <label for="detalle_'+var_id+'">Detalle</label>\
                    <div class="form-line">\
                        <textarea id="detalle_'+var_id+'" class="md-textarea form-control txta-own capacitacion"></textarea>\
                    </div>\
                </div>\
            </div>\
            <div class="col-sm-3">\
                <div class="form-group form-float">\
                    <div class="form-line">\
                        <input id="documento_'+var_id+'" type="text" class="form-control capacitacion">\
                        <label for="documento_'+var_id+'" class="form-label">Documento</label>\
                    </div>\
                </div>\
            </div>\
            <div class="col-sm-2">\
                <div class="form-group">\
                    <div class="form-line">\
                        <label for="fechainicio_'+var_id+'" class="form-label">Fecha Inicio</label>\
                        <input id="fechainicio_'+var_id+'" name="fechainicio" type="text" class="form-control capacitacion date">\
                    </div>\
                </div>\
            </div>\
            <div class="col-sm-2">\
                <div class="form-group">\
                    <div class="form-line">\
                        <label for="fechafin_'+var_id+'" class="form-label">Fecha Fin</label>\
                        <input id="fechafin_'+var_id+'" name="fechafin" type="text" class="form-control capacitacion date">\
                    </div>\
                </div>\
            </div>\
            <div class="col-sm-1">\
                <button type="button" class="btn bg-red waves-effect clear_capacitacion" title="Eliminar">\
                    <i class="material-icons">clear</i>\
                </button>\
            </div>\
        </div>'
    )

    $('.clear_capacitacion').last().click(function () {
        $(this).parent().parent().remove()
    })

    $('.capacitacion').focus(function () {
        $(this).parent().addClass('focused');
    })

    $('.date').bootstrapMaterialDatePicker({
        format: 'DD/MM/YYYY',
        clearButton: false,
        weekStart: 1,
        locale: 'es',
        time: false
    }).on('change', function (e, date) {
        $(this).parent().addClass('focused');
    });

    if(id_in.length > 0){
        $('#detalle_'+var_id).val(id_in[1])
        $('#documento_'+var_id).val(id_in[2])
        $('#fechainicio_'+var_id).val(id_in[3])
        $('#fechafin_'+var_id).val(id_in[4])
    }
}

function append_input_estudio(id_in) {
    if(id_in.length === 0){
        gb_id++;
        var_id = 'nw'+gb_id;
        elem = 0;
    }else{
        var_id = id_in[0];
        elem = id_in[0];
    }

    $('#estudio_div').append(
        '<div class="row">\
            <div class="col-md-1 hidden">\
                <div class="form-group form-float">\
                    <div class="form-line">\
                        <input id="id'+var_id+'" value="'+elem+'" class="form-control estudio readonly">\
                    </div>\
                </div>\
            </div>\
            <div class="col-sm-4">\
                <div class="form-group form-float">\
                    <label for="detallest_'+var_id+'">Detalle</label>\
                    <div class="form-line">\
                        <textarea id="detallest_'+var_id+'" class="md-textarea form-control txta-own estudio"></textarea>\
                    </div>\
                </div>\
            </div>\
            <div class="col-sm-3">\
                <div class="form-group form-float">\
                    <div class="form-line">\
                        <input id="gestion_'+var_id+'" type="text" class="form-control estudio" >\
                        <label for="gestion_'+var_id+'" class="form-label">Gestión</label>\
                    </div>\
                </div>\
            </div>\
            <div class="col-sm-3">\
                <div class="form-group form-float">\
                    <div class="form-line">\
                        <input id="tipo_'+var_id+'" type="text" class="form-control estudio" >\
                        <label for="tipo_'+var_id+'" class="form-label">Tipo</label>\
                    </div>\
                </div>\
            </div>\
            <div class="col-sm-1">\
                <button type="button" class="btn bg-red waves-effect clear_estudio" title="Eliminar">\
                    <i class="material-icons">clear</i>\
                </button>\
            </div>\
        </div>'
    )

    $('.clear_estudio').last().click(function () {
        $(this).parent().parent().remove()
    })

    $('.estudio').focus(function () {
        $(this).parent().addClass('focused');
    })

    if(id_in.length > 0){
        $('#detallest_'+var_id).val(id_in[1])
        $('#gestion_'+var_id).val(id_in[2])
        $('#tipo_'+var_id).val(id_in[3])
    }
}

function append_input_beca(id_in) {
    if(id_in.length === 0){
        gb_id++;
        var_id = 'nw'+gb_id;
        elem = 0;
    }else{
        var_id = id_in[0];
        elem = id_in[0];
    }

    $('#beca_div').append(
        '<div class="row">\
            <div class="col-md-1 hidden">\
                <div class="form-group form-float">\
                    <div class="form-line">\
                        <input id="id'+var_id+'" value="'+elem+'" class="form-control beca readonly">\
                    </div>\
                </div>\
            </div>\
            <div class="col-sm-2">\
                <div class="form-group form-float">\
                    <div class="form-line">\
                        <input id="documentob_'+var_id+'" type="text" class="form-control beca">\
                        <label for="documentob_'+var_id+'" class="form-label">Memo o Resolución</label>\
                    </div>\
                </div>\
            </div>\
            <div class="col-sm-2">\
                <div class="form-group form-float">\
                    <div class="form-line">\
                        <input id="evento_'+var_id+'" type="text" class="form-control beca">\
                        <label for="evento_'+var_id+'" class="form-label">Evento</label>\
                    </div>\
                </div>\
            </div>\
            <div class="col-sm-2">\
                <div class="form-group form-float">\
                    <label for="detalleb_'+var_id+'">Naturaleza</label>\
                    <div class="form-line">\
                        <textarea id="detalleb_'+var_id+'" class="md-textarea form-control txta-own beca"></textarea>\
                    </div>\
                </div>\
            </div>\
            <div class="col-sm-2">\
                <div class="form-group">\
                    <div class="form-line">\
                        <label for="fechainiciob_'+var_id+'" class="form-label">Fecha Inicio</label>\
                        <input id="fechainiciob_'+var_id+'" name="fechainicio" type="text" class="form-control beca date">\
                    </div>\
                </div>\
            </div>\
            <div class="col-sm-2">\
                <div class="form-group">\
                    <div class="form-line">\
                        <label for="fechafinb_'+var_id+'" class="form-label">Fecha Fin</label>\
                        <input id="fechafinb_'+var_id+'" name="fechafin" type="text" class="form-control beca date">\
                    </div>\
                </div>\
            </div>\
            <div class="col-sm-1">\
                <button type="button" class="btn bg-red waves-effect clear_beca" title="Eliminar">\
                    <i class="material-icons">clear</i>\
                </button>\
            </div>\
        </div>'
    )

    $('.clear_beca').last().click(function () {
        $(this).parent().parent().remove()
    })

    $('.beca').focus(function () {
        $(this).parent().addClass('focused');
    })

    $('.date').bootstrapMaterialDatePicker({
        format: 'DD/MM/YYYY',
        clearButton: false,
        weekStart: 1,
        locale: 'es',
        time: false
    }).on('change', function (e, date) {
        $(this).parent().addClass('focused');
    });

    if(id_in.length > 0){
        $('#documentob_'+var_id).val(id_in[1])
        $('#evento_'+var_id).val(id_in[2])
        $('#detalleb_'+var_id).val(id_in[3])
        $('#fechainiciob_'+var_id).val(id_in[4])
        $('#fechafinb_'+var_id).val(id_in[5])
    }
}

function append_input_idioma(id_in) {
    if(id_in.length === 0){
        gb_id++;
        var_id = 'nw'+gb_id;
        elem = 0;
    }else{
        var_id = id_in[0];
        elem = id_in[0];
    }

    $('#idioma_div').append(
        '<div class="row">\
            <div class="col-md-1 hidden">\
                <div class="form-group form-float">\
                    <div class="form-line">\
                        <input id="id'+var_id+'" value="'+elem+'" class="form-control idioma readonly">\
                    </div>\
                </div>\
            </div>\
            <div class="col-sm-6">\
                <div class="form-group form-float">\
                    <div class="form-line">\
                        <input id="idioma_'+var_id+'" type="text" class="form-control idioma" >\
                        <label for="idioma_'+var_id+'" class="form-label">Idioma</label>\
                    </div>\
                </div>\
            </div>\
            <div class="col-sm-1">\
                <div class="form-group form-float">\
                    <input id="habla_'+var_id+'" type="checkbox" class="module chk-col-deep-purple idioma">\
                    <label for="habla_'+var_id+'" class="form-label">Habla</label>\
                </div>\
            </div>\
            <div class="col-sm-1">\
                <div class="form-group form-float">\
                    <input id="lee_'+var_id+'" type="checkbox" class="module chk-col-deep-purple idioma">\
                    <label for="lee_'+var_id+'" class="form-label">Lee</label>\
                </div>\
            </div>\
            <div class="col-sm-1">\
                <div class="form-group form-float">\
                    <input id="escribe_'+var_id+'" type="checkbox" class="module chk-col-deep-purple idioma">\
                    <label for="escribe_'+var_id+'" class="form-label">Escribe</label>\
                </div>\
            </div>\
            <div class="col-sm-1">\
                <div class="form-group form-float">\
                    <input id="aprendio_'+var_id+'" type="checkbox" class="module chk-col-deep-purple idioma">\
                    <label for="aprendio_'+var_id+'" class="form-label">Aprendió</label>\
                </div>\
            </div>\
            <div class="col-sm-1">\
                <button type="button" class="btn bg-red waves-effect clear_idioma" title="Eliminar">\
                    <i class="material-icons">clear</i>\
                </button>\
            </div>\
        </div>'
    )

    $('.clear_idioma').last().click(function () {
        $(this).parent().parent().remove()
    })

    $('.idioma').focus(function () {
        $(this).parent().addClass('focused');
    })

    if(id_in.length > 0){
        $('#idioma_'+var_id).val(id_in[1])
        $('#habla_'+var_id).prop('checked', id_in[2])
        $('#lee_'+var_id).prop('checked', id_in[3])
        $('#escribe_'+var_id).prop('checked', id_in[4])
        $('#aprendio_'+var_id).prop('checked', id_in[5])
    }
}

function append_input_experiencia(id_in) {
    if(id_in.length === 0){
        gb_id++;
        var_id = 'nw'+gb_id;
        elem = 0;
    }else{
        var_id = id_in[0];
        elem = id_in[0];
    }

    $('#experiencia_div').append(
        '<div class="row">\
            <div class="col-md-1 hidden">\
                <div class="form-group form-float">\
                    <div class="form-line">\
                        <input id="id'+var_id+'" value="'+elem+'" class="form-control experiencia readonly">\
                    </div>\
                </div>\
            </div>\
            <div class="col-sm-5">\
                <div class="form-group form-float">\
                    <div class="form-line">\
                        <input id="especialidad_'+var_id+'" type="text" class="form-control experiencia" >\
                        <label for="especialidad_'+var_id+'" class="form-label">Especialidad</label>\
                    </div>\
                </div>\
            </div>\
            <div class="col-sm-5">\
                <div class="form-group form-float">\
                    <div class="form-line">\
                        <input id="entidad_'+var_id+'" type="text" class="form-control experiencia" >\
                        <label for="entidad_'+var_id+'" class="form-label">Entidad</label>\
                    </div>\
                </div>\
            </div>\
            <div class="col-sm-1">\
                <button type="button" class="btn bg-red waves-effect clear_experiencia" title="Eliminar">\
                    <i class="material-icons">clear</i>\
                </button>\
            </div>\
        </div>'
    )

    $('.clear_experiencia').last().click(function () {
        $(this).parent().parent().remove()
    })

    $('.experiencia').focus(function () {
        $(this).parent().addClass('focused');
    })

    if(id_in.length > 0){
        $('#especialidad_'+var_id).val(id_in[1])
        $('#entidad_'+var_id).val(id_in[2])
    }
}

function append_input_hijo(id_in) {
    if(id_in.length === 0){
        gb_id++;
        var_id = 'nw'+gb_id;
        elem = 0;
    }else{
        var_id = id_in[0];
        elem = id_in[0];
    }

    $('#hijo_div').append(
        '<div class="row">\
            <div class="col-md-1 hidden">\
                <div class="form-group form-float">\
                    <div class="form-line">\
                        <input id="id'+var_id+'" value="'+elem+'" class="form-control hijo readonly">\
                    </div>\
                </div>\
            </div>\
            <div class="col-sm-3">\
                <div class="form-group form-float">\
                    <div class="form-line">\
                        <input id="nombre_'+var_id+'" type="text" class="form-control hijo">\
                        <label for="nombre_'+var_id+'" class="form-label">Nombre</label>\
                    </div>\
                </div>\
            </div>\
            <div class="col-sm-3">\
                <div class="form-group form-float">\
                    <div class="form-line">\
                        <input id="direccion_'+var_id+'" type="text" class="form-control hijo">\
                        <label for="direccion_'+var_id+'" class="form-label">Dirección</label>\
                    </div>\
                </div>\
            </div>\
            <div class="col-sm-2">\
                <div class="form-group form-float">\
                    <div class="form-line">\
                        <input id="telefono_'+var_id+'" type="text" class="form-control hijo">\
                        <label for="telefono_'+var_id+'" class="form-label">Teléfono</label>\
                    </div>\
                </div>\
            </div>\
            <div class="col-sm-2">\
                <div class="form-group">\
                    <div class="form-line">\
                        <label for="fechanacimiento_'+var_id+'" class="form-label">Fecha de Nacimiento</label>\
                        <input id="fechanacimiento_'+var_id+'" name="fechanacimiento" type="text" class="form-control hijo date">\
                    </div>\
                </div>\
            </div>\
            <div class="col-sm-1">\
                <button type="button" class="btn bg-red waves-effect clear_hijo" title="Eliminar">\
                    <i class="material-icons">clear</i>\
                </button>\
            </div>\
        </div>'
    )

    $('.clear_hijo').last().click(function () {
        $(this).parent().parent().remove()
    })

    $('.hijo').focus(function () {
        $(this).parent().addClass('focused');
    })

    $('.date').bootstrapMaterialDatePicker({
        format: 'DD/MM/YYYY',
        clearButton: false,
        weekStart: 1,
        locale: 'es',
        time: false
    }).on('change', function (e, date) {
        $(this).parent().addClass('focused');
    });

    if(id_in.length > 0){
        $('#nombre_'+var_id).val(id_in[1])
        $('#direccion_'+var_id).val(id_in[2])
        $('#telefono_'+var_id).val(id_in[3])
        $('#fechanacimiento_'+var_id).val(id_in[4])
    }
}

function append_table_contrato(id) {
    obj = JSON.stringify({
        'id': parseInt(id)
    })
    ajax_call_post_no_msg("persona_contratos", {
        _xsrf: getCookie("_xsrf"),
        object: obj
    }, function(response) {
        var datos = response.response
        var partaux = "";
        var i = 0;
        //console.log('table')
        //console.log(datos)
        //console.log(Object.keys(datos).length)

        if (Object.keys(datos).length > 0) {
            for (a in datos) {
                if (['None', null].includes(datos[i].fechaForzado)) frtf = ''; else frtf = datos[i].fechaForzado;
                if (['None', null].includes(datos[i].fechaFin)) ffin = ''; else ffin = datos[i].fechaFin;
                partaux +=
                    '<tr>' +
                        '<td>' + datos[i].nroContrato + '</td>' +
                        '<td>' + datos[i].persona + '</td>' +
                        '<td>' + datos[i].tipo + '</td>' +
                        '<td>' + datos[i].fechaIngreso + '</td>' +
                        '<td>' + frtf + '</td>' +
                        '<td>' + ffin + '</td>' +
                    '</tr>';

                i++;
            }

            $('#box_contrato').append(
                '<div class="row">\
                        <div class="body table-responsive">\
                            <table id="table_contrato" class="table table-bordered table-striped table-hover">\
                                <thead>\
                                    <tr>\
                                        <th class="order_by_th" data-name="names">Nro. Contrato</th>\
                                        <th class="order_by_th" data-name="names">Nombre Completo</th>\
                                        <th class="order_by_th" data-name="names">Situación Laboral</th>\
                                        <th class="order_by_th" data-name="names">Fecha Ingreso</th>\
                                        <th class="order_by_th" data-name="names">Fecha Retiro Forzado</th>\
                                        <th class="order_by_th" data-name="names">Fecha Retiro</th>\
                                    </tr>\
                                </thead>\
                                <tbody id="table_content">' + partaux + '</tbody>\
                        </table>\
                    </div>\
                </div>'
            );
            $('#table_contrato').DataTable()
        } else {
            $('#box_contrato').append(
                '<div id="no_dtcont" class="container-fluid">No se obtuvo ningún registro.</div>'
            );
        }
    })
}


$('#new-contrato').click(function () {
    $('#content-contrato').show()
    $('#new-contrato').hide()
    $('#close-contrato').show()
    $('#enable_cont').val('true')
    $('#fechafin').attr('required', 'required')

    $('#fechaforzado').parent().parent().hide()
    $('#descripcionc').parent().parent().hide()

    $('#nrocontrato').parent().parent().show()
    $('#tipocont').parent().parent().show()
    $('#sueldo').parent().parent().show()
    $('#fechaingreso').parent().parent().show()
    if($('#tipocont').val() != 'INDEFINIDO') $('#fechafin').parent().parent().show()
});

$('#close-contrato').click(function () {
    //clean_dtcontrato()
    if (gb_ret == 1) {
        $('#new-contrato').hide()
        $('#force-contrato').show()
    } else {
        if (gb_ret == 2) {
            $('#new-contrato').show()
            $('#force-contrato').hide()
        } else {
            $('#new-contrato').show()
            $('#force-contrato').show()
        }
    }
    $('#content-contrato').hide()
    $('#close-contrato').hide()
});

$('#insert-contrato').click(function () {
    var table = $('#table_contrato').DataTable();
    table.clear().draw();

    ajax_call_post('persona_getcontrato',{
        _xsrf: getCookie("_xsrf")
    },function(response){
        var datar = response.response

        for (var i = 0; i < Object.keys(datar).length; i++) {
            if(datar[i]['fechaForzado'] != null) fechaforzado = datar[i]['fechaForzado'];
            else fechaforzado = '';

            table.row.add([
                datar[i]["nroContrato"],
                (datar[i]["persona"]['apellidopaterno']+' '+datar[i]["persona"]['apellidomaterno']+' '+datar[i]["persona"]['nombres']),
                datar[i]['tipo'],
                datar[i]['fechaIngreso'],
                fechaforzado,
                datar[i]['fechaFin']
            ]).draw(false);
        }

        table.row.add([
            $('#nrocontrato').val(),
            ($('#apellidop').val()+' '+$('#apellidom').val()+' '+$('#nombres').val()),
            $('#tipocont').val(),
            $('#fechaingreso').val(),
            $('#fechaforzado').val(),
            $('#fechafin').val()
        ]).draw(false);
    })
    clean_dtcontrato()
    $('#content-contrato').hide()
    table.order([0, 'desc']).draw()
});

function clean_dtcontrato(){
    $('#nrocontrato').val('')
    $('#sueldo').val('')
    $('#fechaingreso').val('')
    $('#fechaforzado').val('')
    $('#fechafin').val('')
    $('#descripcionc').val('')
    $('#tipocont').val('')
    $('#tipocont').selectpicker('refresh')
}

function clean_allform(){
    $('#close-contrato').click()

    $('.persona').val('')
    $('.persona').selectpicker('refresh')

    $('.empleado').val('')
    $('.empleado').selectpicker('refresh')

    $('.administrativo').val('')
    $('.administrativo').selectpicker('refresh')

    $('.educacion').val('')
    $('.educacion').selectpicker('refresh')

    $('.padres').val('')
    $('.padres').selectpicker('refresh')

    $('.conyuge').val('')
    $('.conyuge').selectpicker('refresh')

    $('.contrato').val('')
    $('.contrato').selectpicker('refresh')

    $('#capacitacion_div').empty();
    $('#estudio_div').empty();
    $('#beca_div').empty();
    $('#idioma_div').empty();
    $('#experiencia_div').empty();
    $('#hijo_div').empty();
}

$('#new').click(function () {
    $('.fileinput-remove-button').click()
    $('#show_img').parent().parent().hide()
    $('#fechaforzado').parent().parent().hide()
    $('#descripcionc').parent().parent().hide()
    // $('#fechafin').attr('required', 'required')

    if ($.fn.DataTable.isDataTable('#table_contrato')) {
        var del_cont = $('#table_contrato').DataTable()
        del_cont.destroy()
        $('#box_contrato').empty()
    }
    clean_allform()
    verif_inputs('')
    gb_ret = 2

    $('#id_div').hide()
    $('#idctr_div').hide()
    $('#insert').show()
    $('#update').hide()
    $('.nav-tabs li > a:first').tab('show')
    validationInputSelects("form")
    $('#content-contrato').hide()
    $('#close-contrato').hide()
    $('#force-contrato').hide()
    $('#new-contrato').show()
    $('#form').modal('show')
})

function valid_dataform(){
    var object_inputs = $('.persona')

    h1 = object_inputs[1].value;
    h2 = object_inputs[2].value;
    h3 = object_inputs[3].value;
    h4 = object_inputs[4].value;
    h5 = object_inputs[6].value;
    h6 = object_inputs[8].value;

    items = [h1, h2, h3, h4, h5, h6];
    resp = !item_is_empty(items);

    var object_inputs_emp = $('.empleado')

    h7 = object_inputs_emp[2].value;

    items_emp = [h7];
    resp_emp = !item_is_empty(items_emp);

    if(!resp){
        if(gb_msg.length > 0) gb_msg += ' datos generales';
        else gb_msg += 'datos generales';
    }

    if(!resp_emp){
        if(gb_msg.length > 0) gb_msg += ' código';
        else gb_msg += 'código';
    }

    return resp && resp_emp;
}

$('#submit_form').on('submit', function (e) {
    e.preventDefault();
    values = "";
    var data = new FormData($(this)[0]);
    gb_msg = '';

    notvalid = validationInputSelectsWithReturn("form");
    if (notvalid === false) {
        if($('#id').val() === '') {
            objeto = JSON.stringify({
                'apellidopaterno': $('#apellidop').val(),
                'apellidomaterno': $('#apellidom').val(),
                'nombres': $('#nombres').val(),
                'sexo': $('#sexo').val(),
                'ci': $('#ci').val(),
                'fechanacimiento': $('#fechanacimiento').val(),
                'domicilio': $('#domicilio').val(),
                'telefono': $('#telefonodt').val(),

                'enabled': true,
                'empleado': get_empleado(),
                'contrato': get_contrato(),
                'administrativo': get_administrativo(),
                'educacion': get_educacion(),
                'capacitacion': get_capacitacion(),
                'estudios': get_estudio(),
                'memo': get_beca(),
                'idioma': get_idioma(),
                'experiencia': get_experiencia(),
                'padres': get_padres(),
                'conyuge': get_conyuge(),
                'hijos': get_hijos()
            })
        } else {
            objeto = JSON.stringify({
                'id': parseInt($('#id').val()),
                'apellidopaterno': $('#apellidop').val(),
                'apellidomaterno': $('#apellidom').val(),
                'nombres': $('#nombres').val(),
                'sexo': $('#sexo').val(),
                'ci': $('#ci').val(),
                'fechanacimiento': $('#fechanacimiento').val(),
                'domicilio': $('#domicilio').val(),
                'telefono': $('#telefonodt').val(),
                'enabled': true,
                'empleado': get_empleado(),
                'contrato': get_contrato(),
                'administrativo': get_administrativo(),
                'educacion': get_educacion(),
                'capacitacion': get_capacitacion(),
                'estudios': get_estudio(),
                'memo': get_beca(),
                'idioma': get_idioma(),
                'experiencia': get_experiencia(),
                'padres': get_padres(),
                'conyuge': get_conyuge(),
                'hijos': get_hijos()
            })
        }

        ruta = 'persona_insert';
        //console.log(JSON.parse(objeto));

        data.append('object', objeto)
        data.append('_xsrf', getCookie("_xsrf"))
        render = null
        callback = function () {
            setTimeout(function () {
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
                if ("message" in dictionary && dictionary.message !== '') {
                    if (dictionary.success) showMessage(dictionary.message, "success", "ok")
                    else showMessage(dictionary.message, "danger", "remove")
                }
            }
            if (callback != null)  callback(response)
        })
        $('#form').modal('hide')
    } else {
        swal('Error de datos.', notvalid, 'error')
    }
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
    $('#insert').show()
    $('#update').hide()
    $('#form-importar').modal('show')
})


function attach_edit() {
    $('.edit').click(function () {
        clean_allform()
        $('#no_dtcont').remove()
        $('#close-contrato').hide()
        $('#content-contrato').hide()
        gb_ret = 0;
        document.getElementById("tab-dtpersonal").click();
        obj = JSON.stringify({
            'id': parseInt(JSON.parse($(this).attr('data-json')))
        })

        ajax_call_get('persona_update', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            //console.log(response)
            gb_obj = {}

            if (!self.enabled) {
                $('#new-contrato').show()
                $('#force-contrato').hide()
                gb_ret = 2;
                $('#enable_cont').val('true')
            }
            $('#id').val(self.id)
            $('#apellidop').val(self.apellidopaterno)
            $('#apellidom').val(self.apellidomaterno)
            $('#nombres').val(self.nombres)
            $('#fechanacimiento').val(self.fechanacimiento)
            $('#ci').val(self.ci)
            if (self.domicilio !== 'None') $('#domicilio').val(self.domicilio)
            if (self.telefono !== 'None') $('#telefonodt').val(self.telefono)
            

            $('#sexo').val(self.sexo)
            $('#sexo').selectpicker('refresh')
            cargar_datos_administrativos(self)
            $('#box_contrato').empty();
            append_table_contrato(self.id)

            if (self.empleado.length > 0) {
                $('#idemp').val(self.empleado[0].id)
                $('#codigo').val(self.empleado[0].codigo)
                $('#nrocontrato').val(self.empleado[0].codigo)

                if (!['None', null].includes(self.empleado[0].email)) $('#email').val(self.empleado[0].email)

                $('#fksucursal').val(self.empleado[0].fksucursal)
                $('#fksucursal').selectpicker('refresh')

                if (self.empleado[0].fkoficina !== 'None') {
                    $('#fkoficina').val(self.empleado[0].fkoficina)
                    $('#fkoficina').selectpicker('refresh')
                }

                $('#fkgerencia').val(self.empleado[0].fkgerencia)
                $('#fkgerencia').selectpicker('refresh')

                $('#fkcargo').val(self.empleado[0].fkcargo)
                $('#fkcargo').selectpicker('refresh')

                $('#fkcentro').val(self.empleado[0].fkcentro)
                $('#fkcentro').selectpicker('refresh')

                if(self.empleado[0].foto.includes('images/personal')){
                    $('#show_img').attr('src', self.empleado[0].foto);
                    $('#show_img').parent().parent().show();
                }else{
                    $('#show_img').attr('src', '/resources/images/no_photo.png');
                    $('#show_img').parent().parent().show();
                }
            }

            if(self.contrato.length > 0) {
                for (i = 0; i < self.contrato.length; i++) {
                   if (self.contrato[i].enabled) {
                        var nulos = ['None', null, ''];

                        $('#idctr').val(self.contrato[i].id)
                        $('#nrocontrato').val(self.contrato[i].nroContrato)
                        if (!nulos.includes(self.contrato[i].sueldo)) $('#sueldo').val(self.contrato[i].sueldo); else $('#sueldo').val(0);
                        $('#fechaingreso').val(self.contrato[i].fechaIngreso)
                        if (!nulos.includes(self.contrato[i].fechaForzado)) $('#fechaforzado').val(self.contrato[i].fechaForzado)

                        $('#tipocont').val(self.contrato[i].tipo)
                        $('#tipocont').selectpicker('refresh')

                        if (self.contrato[i].tipo === 'INDEFINIDO') $('#fechafin').parent().parent().hide()
                        else $('#fechafin').parent().parent().show()
                        if (self.contrato[0].tipo !== 'INDEFINIDO') {
                            if (!nulos.includes(self.contrato[i].fechaFin)) {
                                var dt = new Date();
                                var parts = (self.contrato[i].fechaFin).split('/');
                                //console.log(parts)
                                var fd = (parts[0].indexOf('0') === 0)? parts[0].replace('0', ''): parts[0];
                                var fm = (parts[1].indexOf('0') === 0)? parts[1].replace('0', ''): parts[1];
                                //console.log('no indef - ffin dt');
                                //console.log(fd+' | '+fm);
                                var df = new Date(parts[2]+'-'+fm+'-'+fd);
                                //console.log(dt.getFullYear()+'-'+(dt.getMonth()+1)+'-'+dt.getDate())
                                //console.log(df.getFullYear()+'-'+(df.getMonth()+1)+'-'+df.getDate())

                                if (dt > df) {
                                    $('#force-contrato').show()
                                    $('#new-contrato').hide()
                                    gb_ret = 1;
                                    $('#enable_cont').val('false')
                                    //console.log('end vig')
                                } else {
                                    $('#force-contrato').show()
                                    $('#new-contrato').show()
                                    $('#enable_cont').val('true')
                                    //console.log('still vig')
                                }
                            } else {
                                console.log("true")
                                $('#force-contrato').show()
                                $('#new-contrato').show()
                                $('#enable_cont').val('true')
                            }
                        } else {
                            $('#force-contrato').show()
                            $('#new-contrato').show()
                            $('#enable_cont').val('true')
                            //console.log('indef')
                        }

                        $('#fechafin').val(self.contrato[i].fechaFin)
                        if (self.contrato[i].descripcion !== 'None') $('#descripcionc').val(self.contrato[i].descripcion)

                        $('#fechaforzado').parent().parent().hide()
                        $('#descripcionc').parent().parent().hide()
                    }
                }
            }

            if(self.administrativo.length > 0) {
                $('#idadm').val(self.administrativo[0].id)
                $('#nroasegurado').val(self.administrativo[0].nroAsegurado)
                $('#cajasalud').val(self.administrativo[0].cajaSalud)
                $('#afp').val(self.administrativo[0].afp)

                $('#tipotrabajador').val(self.administrativo[0].tipoTrabajador)
                $('#tipotrabajador').selectpicker('refresh')
                $('#banco').val(self.administrativo[0].banco)
                $('#banco').selectpicker('refresh')

                $('#nrocuenta').val(self.administrativo[0].nroCuenta)
                $('#libretamilitar').val(self.administrativo[0].libretaMilitar)
                $('#hijos').val(self.administrativo[0].hijos)
                $('#hijos').selectpicker('refresh')

                $('#brevete').val(self.administrativo[0].brevete)
                $('#gruposanguineo').val(self.administrativo[0].grupoSanguineo)
                $('#telefonofijo').val(self.administrativo[0].telefonoFijo)
                $('#telefonocelular').val(self.administrativo[0].telefonoCelular)
                $('#estadocivil').val(self.administrativo[0].estadoCivil)
                $('#estadocivil').selectpicker('refresh')

                $('#nacimientopais').val(self.administrativo[0].nacimientoPais)
                $('#nacimientodepartamento').val(self.administrativo[0].nacimientoDepartamento)
                $('#nacimientoprovincia').val(self.administrativo[0].nacimientoProvincia)
                $('#nacimientodistrito').val(self.administrativo[0].nacimientoDistrito)
                $('#nacimientodomicilio').val(self.administrativo[0].nacimientoDomicilio)
                $('#domiciliopais').val(self.administrativo[0].domicilioPais)
                $('#domiciliodepartamento').val(self.administrativo[0].domicilioDepartamento)
                $('#domicilioprovincia').val(self.administrativo[0].domicilioProvincia)
                $('#domiciliodistrito').val(self.administrativo[0].domicilioDistrito)
                $('#domiciliodireccion').val(self.administrativo[0].domiciliodireccion)

                $('#domiciliocasa').val(self.administrativo[0].domicilioCasa)
                $('#domiciliocasa').selectpicker('refresh')
            }

            if(self.educacion.length > 0) {
                $('#idedc').val(self.educacion[0].id)

                $('#niveleducativo').val(self.educacion[0].nivelEducativo)
                $('#niveleducativo').selectpicker('refresh')

                $('#tipocentroestudio').val(self.educacion[0].tipoCentroEstudio)
                $('#tipocentroestudio').selectpicker('refresh')

                $('#condicionactual').val(self.educacion[0].condicionActual)
                $('#condicionactual').selectpicker('refresh')

                $('#nombrecentroestudio').val(self.educacion[0].nombreCentroEstudio)
                $('#profesiondt').val(self.educacion[0].profesion)
                $('#fechatitulodt').val(self.educacion[0].fechaTitulo)
            }

            if(self.conyuge.length > 0) {
                $('#idcon').val(self.conyuge[0].id)
                $('#nombre').val(self.conyuge[0].nombreCompleto)
                $('#fechanacimientocyg').val(self.conyuge[0].fechanacimiento)
                $('#cicyg').val(self.conyuge[0].ci)

                $('#sexoc').val(self.conyuge[0].sexo)
                $('#sexoc').selectpicker('refresh')

                $('#pais').val(self.conyuge[0].pais)
                $('#departamento').val(self.conyuge[0].departamento)
                $('#provincia').val(self.conyuge[0].provincia)
                $('#distrito').val(self.conyuge[0].distrito)
                $('#profesion').val(self.conyuge[0].profesion)
                $('#domiciliocyg').val(self.conyuge[0].domicilio)
                $('#telefonoc').val(self.conyuge[0].telefono)
                $('#instruccion').val(self.conyuge[0].instruccion)
                $('#ocupacion').val(self.conyuge[0].ocupacion)
                $('#centrotrabajo').val(self.conyuge[0].centroTabajo)
            }

            if(self.padres.length > 0) {
                for (cp = 0; cp < self.padres.length; cp++){
                    if(self.padres[cp].tipo == 'Padre'){
                        $('#idp').val(self.padres[cp].id)
                        $('#nombrecompletop').val(self.padres[cp].nombreCompleto)
                        $('#fechanacimientop').val(self.padres[cp].fechanacimiento)
                        $('#telefenop').val(self.padres[cp].telefono)

                        $('#situacionp').val(self.padres[cp].situacion)
                        $('#situacionp').selectpicker('refresh')
                    }else{
                        $('#idm').val(self.padres[cp].id)
                        $('#nombrecompletom').val(self.padres[cp].nombreCompleto)
                        $('#fechanacimientom').val(self.padres[cp].fechanacimiento)
                        $('#telefenom').val(self.padres[cp].telefono)

                        $('#situacionm').val(self.padres[cp].situacion)
                        $('#situacionm').selectpicker('refresh')
                    }
                }
            }

            if(self.capacitacion.length > 0) {
                for (ct = 0; ct < self.capacitacion.length; ct++){
                    datacp = [self.capacitacion[ct].id, self.capacitacion[ct].detalle, self.capacitacion[ct].documento,
                                self.capacitacion[ct].fechaInicio, self.capacitacion[ct].fechaFin];
                    append_input_capacitacion(datacp)
                }
            }

            if(self.estudios.length > 0) {
                for (cs = 0; cs < self.estudios.length; cs++){
                    datast = [self.estudios[cs].id, self.estudios[cs].detalle, self.estudios[cs].gestion, self.estudios[cs].tipo];
                    append_input_estudio(datast)
                }
            }

            if(self.memo.length > 0) {
                for (cb = 0; cb < self.memo.length; cb++){
                    databc = [self.memo[cb].id, self.memo[cb].documento, self.memo[cb].evento, self.memo[cb].detalle,
                            self.memo[cb].fechaInicio, self.memo[cb].fechaFin];
                    append_input_beca(databc)
                }
            }

            if(self.idioma.length > 0) {
                for (cd = 0; cd < self.idioma.length; cd++){
                    datalng = [self.idioma[cd].id, self.idioma[cd].idioma, self.idioma[cd].habla, self.idioma[cd].lee,
                            self.idioma[cd].escribe, self.idioma[cd].aprendio];
                    append_input_idioma(datalng)
                }
            }

            if(self.experiencia.length > 0) {
                for (cx = 0; cx < self.experiencia.length; cx++){
                    dataexp = [self.experiencia[cx].id, self.experiencia[cx].especialidad, self.experiencia[cx].entidad];
                    append_input_experiencia(dataexp)
                }
            }

            if(self.hijos.length > 0) {
                for (ch = 0; ch < self.hijos.length; ch++){
                    datachild = [self.hijos[ch].id, self.hijos[ch].nombrecompleto, self.hijos[ch].direccion,
                            self.hijos[ch].telefono, self.hijos[ch].fechanacimiento];
                    append_input_hijo(datachild)
                }
            }

            clean_form()
            verif_inputs('')
            $('#id_div').hide()
            $('#idctr_div').hide()
            $('#insert').hide()
            $('#update').show()
            $('#form').modal('show')
        })
        //console.log(gb_ret)
    })
}
attach_edit()


function attach_edit2() {
    $('.delete').click(function () {
        id = parseInt(JSON.parse($(this).attr('data-json')))
        enabled = false
        swal({
            title: "¿Desea dar de baja al persona?",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#1565c0",
            cancelButtonColor: "#F44336",
            confirmButtonText: "Aceptar",
            cancelButtonText: "Cancelar"
        }).then(function () {
            ajax_call("{{privileges['persona_delete'].route}}", {
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
}
attach_edit2()


$('#importar-form').on('submit', function (e) {
    $('.page-loader-wrapper').show();
    var data = new FormData($(this)[0]);
    data.append('_xsrf', getCookie("_xsrf"))

    $.ajax({
        url: 'persona_importar',
        type: "post",
        data: data,
        contentType: false,
        processData: false,
        cache: false
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
                query_render('/persona');
            });
        }
    });
    e.preventDefault();
});
reload_form()


$('#reporte-xls').click(function () {
    aux = {'datos': table_pdf}
    obj = JSON.stringify(aux)
    ruta = "/persona_reporte_xls";
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


$('.delete').click(function () {
    id = parseInt(JSON.parse($(this).attr('data-json')))
    enabled = false
    swal({
        title: "¿Desea dar de baja los datos de la persona?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#1565c0",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    }).then(function () {
        ajax_call('persona_delete', {
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

validationKeyup("form")
validationSelectChange("form")

$('#tipocont').change(function () {
    if ($(this).val() == 'INDEFINIDO') {
        $('#fechafin').parent().parent().hide();
        $('#fechafin').removeAttr('required');
    }
    else {
        $('#fechafin').parent().parent().show();
        $('#fechafin').attr('required', 'required');
    }
});

$('#list-contrato').click(function () {
    $('#home-tab').click()
    ajax_call_post('persona_listvig', {
        _xsrf: getCookie("_xsrf"),
        object: null
    }, function (respvg) {
        var contvg = respvg.response;
        ajax_call_post('persona_listcon', {
            _xsrf: getCookie("_xsrf"),
            object: null
        }, function (respcn) {
            var contcn = respcn.response;
            //console.log(contvg)
            //console.log(contcn)

            if ($.fn.DataTable.isDataTable('#list_contvg')) {
                var del_vig = $('#list_contvg').DataTable()
                del_vig.destroy()
            }
            if ($.fn.DataTable.isDataTable('#list_contcn')) {
                var del_cnl = $('#list_contcn').DataTable()
                del_cnl.destroy()
            }

            $('#list_contvg').DataTable({
                data: contvg,
                responsive: true,
                columns: [
                    { title: "Nro. Contrato", data: "nroContrato" },
                    { title: "Nombre Completo", data: "persona.fullname" },
                    { title: "Situación Laboral", data: "tipo" },
                    { title: "Fecha Ingreso", data: "fechaIngreso" },
                    { title: "Fecha Retiro Forzado", data: "fechaForzado" },
                    { title: "Fecha Retiro", data: "fechaFin" }
                ]
            });

            $('#list_contcn').DataTable({
                data: contcn,
                responsive: true,
                columns: [
                    { title: "Nro. Contrato", data: "nroContrato" },
                    { title: "Nombre Completo", data: "persona.fullname" },
                    { title: "Situación Laboral", data: "tipo" },
                    { title: "Fecha Ingreso", data: "fechaIngreso" },
                    { title: "Fecha Retiro Forzado", data: "fechaForzado" },
                    { title: "Fecha Retiro", data: "fechaFin" }
                ]
            });
        })
    })

    $('#personal-cont').modal('show')
});

$('#valid-contrato').click(function () {
    ajax_call_post('persona_validcont ', {
        _xsrf: getCookie("_xsrf"),
        object: null
    }, function (response) {
        var dtresp = response.response
        //console.log(dtresp)
        if (dtresp.message === 'success') {
            showMessage('Acción realizada exitosamente.', "success", "ok")
            setTimeout(function () {
                window.location = main_route
            }, 2000);
        }
        else showMessage('No se pudo realizar la acción.', "danger", "remove")
    })
});

$('#close-list').click(function () {
    $('#personal-cont').modal('hide')
});

$('#home-tab').click(function () {
    $('#body-vig').css("display", "block")
    $('#body-cnl').css("display", "none")
})

$('#profile-tab').click(function () {
    $('#body-vig').css("display", "none")
    $('#body-cnl').css("display", "block")
})

$("#codigo").change(function() {
   $('#nrocontrato').val($(this).val());
   $('#nrocontrato').parent().removeClass('error');

   $('#nrocontrato').parent().addClass('focused');
   $('#errorMsg_nrocontrato').remove()
});

$('#force-contrato').click(function () {
    $('#content-contrato').show()
    $('#new-contrato').hide()
    $('#close-contrato').show()
    $('#fechaforzado').parent().parent().show()
    $('#descripcionc').parent().parent().show()
    //console.log('into force')
    //console.log(gb_obj)
    $('#enable_cont').val('false')
    $('#fechafin').removeAttr('required')

    $('#nrocontrato').parent().parent().hide()
    $('#tipocont').parent().parent().hide()
    $('#sueldo').parent().parent().hide()
    $('#fechaingreso').parent().parent().hide()
    $('#fechafin').parent().parent().hide()
});
