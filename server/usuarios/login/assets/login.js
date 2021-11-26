$( document ).ready(function() { });

$(function () {
   
    $('#sign_in').validate({
        
        highlight: function (input) {
            $(input).parents('.form-line').addClass('error');
        },
        unhighlight: function (input) {
            $(input).parents('.form-line').removeClass('error');
        },
        errorPlacement: function (error, element) {
            $(element).parents('.input-group').append(error);
        }
    });
});

$('#see-pass').mousedown(function(){
    // $("#ic-pass").css("color", "lightgrey");
    $("#password").prop("type", "text");
    // $("#ic-pass").html("visibility");
    document.getElementById("ic-pass").src = "/resources/iconos/ojo_abierto.ico";
});

$("#see-pass").mouseup(function(){
    // $("#ic-pass").css("color", "grey");
    $("#password").prop("type", "password");
    // $("#ic-pass").html("visibility_off");
    document.getElementById("ic-pass").src = "/resources/iconos/ojo_cerrado.ico";
});

function validar(){
  
    if($('#username').val() == '' && $('#password').val() == ''){
        $('#msg-data').fadeIn('slow')
        return false
    }else{
        $('#msg-data').fadeOut('slow')
        return true
    }
}

$('#sign_in').submit(function(){
   
    if(!$('#username').val() == '' && $(!'#password').val() == ''){
        $('#btn-login').html('Espere...')
        $('#msg-data').fadeOut('slow')
    }else{
        $('#msg-data').fadeIn('slow')
    }

});

$('#insert').on('click',function (e) {
    e.preventDefault();
    obj = JSON.stringify({
        'username': $('#username').val(),
        'password': $('#password').val()
    })
    ajax_call_get('usuario_autenticacion', {
        _xsrf: getCookie("_xsrf"),
        object: obj
    }, function (response) {
        var self = response;

        if(self['respuesta']){

            if(self['autenticacion']){

                $('#msg-data-autenticacion').fadeOut('slow')
                $('#sign_in').fadeOut('slow')
                // $('#sign_in').modal('hide')
                $('#autenticacion').fadeIn('slow')
                // $('#autenticacion').modal('show')


            }else{
                console.log("autenticacion false")
                    ajax_call_login('/login', {
                        _xsrf: getCookie("_xsrf"),
                        object: obj
                    }, function () {
                        
                    })
                    setTimeout(function () {
                        window.location = "/"
                    }, 500);

            }

            // $('#msg-data-autenticacion').fadeOut('slow')
            // $('#sign_in').fadeOut('slow')
            // // $('#sign_in').modal('hide')
            // $('#autenticacion').fadeIn('slow')
            // // $('#autenticacion').modal('show')


        }else{
            $('#msg-data').fadeIn('slow')
            setTimeout(function () {
               $('#msg-data').fadeOut('slow')
            }, 2000);

        }


    })



 })

$('#insert_token').on('click',function (e) {
    e.preventDefault();
    obj = JSON.stringify({
        'username': $('#username').val(),
        'password': $('#password').val(),
        'token': $('#token').val(),
    })
    ajax_call_get('usuario_validacion_token', {
        _xsrf: getCookie("_xsrf"),
        object: obj
    }, function (response) {
        var self = response;

        if(self['respuesta']){
            console.log("login true")

            ajax_call_login('/login', {
                _xsrf: getCookie("_xsrf"),
                object: obj
            }, function () {

            })
            setTimeout(function () {
                window.location = "/"
            }, 1500);

        }else{
            console.log("respuesta false")
            $('#msg-data-autenticacion').fadeIn('slow')
        }

    })

 })



$('#envio_email').on('click',function (e) {
    e.preventDefault();
    obj = JSON.stringify({
        'username': $('#username').val(),
        'password': $('#password').val()
    })
    ajax_call_get('usuario_notificacion_token_email', {
        _xsrf: getCookie("_xsrf"),
        object: obj
    }, function (response) {
        var self = response;

        if(self['respuesta']){

            $('#msg-data_correo_ok').fadeIn('slow')
            setTimeout(function () {
               $('#msg-data_correo_ok').fadeOut('slow')
            }, 2000);


        }else{
            console.log(self['mensaje'])
            $('#msg-data_correo_fail').fadeIn('slow')
            setTimeout(function () {
               $('#msg-data_correo_fail').fadeOut('slow')
            }, 2000);
        }

    })

 })

$('#envio_sms').on('click',function (e) {
    e.preventDefault();
    obj = JSON.stringify({
        'username': $('#username').val(),
        'password': $('#password').val()
    })
    ajax_call_get('usuario_notificacion_token_sms', {
        _xsrf: getCookie("_xsrf"),
        object: obj
    }, function (response) {
        var self = response;
        
        if(self['respuesta']){

            $('#msg-data_sms_ok').fadeIn('slow')
            setTimeout(function () {
               $('#msg-data_sms_ok').fadeOut('slow')
            }, 2000);


        }else{
            console.log(self['mensaje'])
            $('#msg-data_sms_fail').fadeIn('slow')
            setTimeout(function () {
               $('#msg-data_sms_fail').fadeOut('slow')
            }, 2000);
        }

    })

 })

$('#envio_ambos').on('click',function (e) {
    e.preventDefault();
    obj = JSON.stringify({
        'username': $('#username').val(),
        'password': $('#password').val()
    })
    ajax_call_get('usuario_notificacion_token_email', {
        _xsrf: getCookie("_xsrf"),
        object: obj
    }, function (response) {
        var self = response;

    })

 })


$('#atras').on('click',function (e) {
    $('#msg-data').fadeOut('slow')
    $('#sign_in').fadeIn('slow')
    // $('#sign_in').modal('hide')
    $('#autenticacion').fadeOut('slow')
    // $('#autenticacion').modal('show')
      e.preventDefault();

 })