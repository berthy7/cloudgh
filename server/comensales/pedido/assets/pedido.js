main_route = '/portal_pedido'

validationKeyup("form")
validationSelectChange("form")
var cont = 0;

$(document).ready(function () {
    $('#data_table').DataTable();
});

$(document).ajaxStart(function () { });

$(document).ajaxStop(function () {
    $.Toast.hideToast();
});

 //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function append_input_plato(pla) {
    $('#plato_div').append(
        '<div class="row">\
            <div class="col-md-1" hidden>\
                <div class="form-line">\
                    <input id="id'+pla+'" class="form-control plato" readonly>\
                </div>\
            </div>\
            <div  class="col-md-8">\
                <div class="form-line">\
                    <div class="form-line"><input id="pla_'+pla+'" type="text" class="form-control plato" readonly></div>\
                </div>\
            </div>\
        </div>'
    )

    $('.clear_plato').last().click(function () {
        $(this).parent().parent().remove()
    })

    $('.examen').selectpicker({
       size: 10,
       liveSearch: true,
       liveSearchPlaceholder: 'Buscar Control de Salud',
       title: 'Seleccione un Control de Salud.'
    })
}

$('#nuevo').click(function () {
    append_input_plato('')
})

function obtener_plato() {
    objeto = []
    objeto_inputs = $('.plato')

    for(i=0;i<objeto_inputs.length;i+=2){
        h0 = objeto_inputs[i].value
        h1 = objeto_inputs[i + 1].value

        if (h1 = 0) {
            return false;
        }


        objeto.push((function add_objeto(h0, h1) {
            if (h0 ==''){
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
            objeto_inputs[i].value,
            objeto_inputs[i + 1].value))
        }
    return objeto
}
///////////////////////////////////////////////////////////////////////////////////////////////////////////////
function cargar_plato_div(self) {
    for (i in self.menuplato) {
        aux = self.menuplato[i].id
        aux1= self.menuplato[i].plato.nombre

        append_input_plato(aux)
        $('#id'+aux).val(aux)
        $('#pla_' + aux).val(aux1)
    }
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
$('#nuevo_pedido').click(function () {
    append_input_pedido('')
})


function obtener_pedido() {
    objeto = []
    objeto_inputs = $('.pedido')

    for(i=0;i<objeto_inputs.length;i+=6){
        h0 = objeto_inputs[i].value
        h1 = objeto_inputs[i + 2].value
        h2 = objeto_inputs[i + 3].checked
        h3 = objeto_inputs[i + 5].value

        objeto.push((function add_objeto(h0,h1,h2,h3) {
            if (h0 ==''){
                return {
                    'fkpersona': h1,
                    'sopa': h2,
                    'fkplato': h3
                }
            }else{
                return {
                    'id':h0,
                    'fkpersona': h1,
                    'sopa': h2,
                    'fkplato': h3
                }
            }
        })(
                h0,
                h1,
                h2,
                h3
        ))
    }
    return objeto
}
///////////////////////////////////////////////////////////////////////////////////////////////////////////////
function cargar_pedido_div(self) {
    for (i in self.menuplato) {
        aux = self.menuplato[i].id
        aux1= self.menuplato[i].fkplato

        append_input_pedido(aux)
        $('#id'+aux).val(aux)
        $('#pla_' + aux).val(aux1)
    }
}


function cargar_menu() {
    ruta = "menu_dia";
    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf")},
        async: false
    }).done(function (response) {
        response = JSON.parse(response)
        var self = response.response;

        $('#idmenu').val(self.id)
        $('#nombre').val(self.nombre)
        $('#fecha').val(self.fecha)
        if (self.foto != "None" && self.foto != "") {
            var img = document.createElement('img');
            img.src = self.foto;
            imagen = document.getElementById('imagen_archivo').appendChild(img);
            imagen.onclick = function(){imagenfoto(self.foto)};
            imagen.width = 200;
            imagen.width = 200;
        } else {
            var img = document.createElement('img');
            img.src = "/resources/images/sinImagen.jpg";
            imagen = document.getElementById('imagen_archivo').appendChild(img);
            imagen.onclick = function(){imagenfoto("/resources/images/sinImagen.jpg")};
            imagen.width = 150;
            imagen.width = 150;
        }
        $('#plato_div').empty()

        cargar_plato_div(self)
    })
}


$('#new').click(function () {
    $('#imagen_archivo').empty()
    cargar_menu()
    FechaActual()

    $('#pedido_div').empty()
    append_input_pedido('')


    verif_inputs('')
    validationInputSelects("form")
    $('#id_div').hide()
    $('#insert').show()
    $('#update').hide()
    $('#form').modal('show')
})


$('#insert').click(function () {
    notvalid = validationInputSelectsWithReturn("form");
    if (notvalid===false) {
        objeto = JSON.stringify({
            'fkmenu': parseInt($('#idmenu').val()),
            'pedidos': obtener_pedido()
        })
        ajax_call('pedido_insert', {
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
        ajax_call_get('pedido_update', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            cont = 0
            var ch;

            cargar_menu()
            aux = self.id
            aux1= self.fkpersona
            aux2= self.sopa
            aux3= self.fkplato

            $('#pedido_div').empty()
            append_input_pedido(aux)

            $('#id'+aux).val(aux)
            $('#per_' + aux).val(aux1)
            $('#b_'+ aux).prop('checked', aux2)
            $('#seg_' + aux).val(aux3)

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
            'fkmenu': parseInt($('#idmenu').val()),
            'pedidos': obtener_pedido()
        })
        ajax_call('pedido_update', {
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
            'Hay campos vacíos por favor verifique sus datos.',
            'error'
        )
    }
})
reload_form()


$('.delete').click(function () {
    id = parseInt(JSON.parse($(this).attr('data-json')))
    enabled = $(this).is(':checked')
    swal({
        title: "¿Desea eliminar el pedido?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#1565c0",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    }).then(function () {
        ajax_call('pedido_delete', {
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

function imagenfoto(foto) {
$('#imagen_grande').empty()

    var imgGrande = document.createElement('img');
    imgGrande.src = foto;
    imagenGrande = document.getElementById('imagen_grande').appendChild(imgGrande);
    imagenGrande.onclick = function(){volverMenu(self.foto)};
    imagenGrande.width = 500;
    imagenGrande.width = 500;


    $('#insert').hide()
    $('#update').hide()
    $('.modal-body-foto').show()
    $('.modal-body').hide()
    $('#form').modal('show')

}

function volverMenu() {

    $('#id_div').hide()
    $('#insert').show()
    $('#update').hide()
    $('.modal-body-foto').hide()
    $('.modal-body').show()

}

function FechaActual() {
    $("#fecha").val(moment().format('DD/MM/YYYY'));
}

validationKeyup("form");
validationSelectChange("form");