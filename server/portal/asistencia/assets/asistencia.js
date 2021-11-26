main_route = '/portal_asistencia'


$(document).ready(function () {


    if ("geolocation" in navigator){ //check geolocation available
        //try to get user current location using getCurrentPosition() method
        navigator.geolocation.getCurrentPosition(function(position){
                console.log("Found your location nLat : "+position.coords.latitude+" nLang :"+ position.coords.longitude);
                localStorage.setItem('latitud',position.coords.latitude)
                localStorage.setItem('longitud',position.coords.longitude)
                console.log(localStorage.getItem("latitud"))
                console.log(localStorage.getItem("longitud"))

                $("#iframe").attr("src", "portal/asistencia/views/mapa.html")
        });
    }else{
        console.log("Browser doesn't support geolocation!");
    }
});

    var constraints = {
    video: {
            width: 250, height: 250
            }
    };

  var streaming = false,
      video        = document.querySelector('#video'),
      canvasf       = document.querySelector('#canvas'),
      photo        = document.querySelector('#photo'),
      startbutton  = document.querySelector('#startbutton'),
      width = 250,
      height = 0;

function cargar_tabla(data){

    if ( $.fn.DataTable.isDataTable( '#data_table' ) ) {
        var table = $('#data_table').DataTable();
        table.destroy();
    }

    $('#data_table').DataTable({
        data:           data,
        deferRender:    true,
        scrollCollapse: true,
        scroller:       true,

        dom: "Bfrtip" ,
        buttons: [
            // {  extend : 'excelHtml5',
            //    exportOptions : { columns : [0, 1, 2, 3, 4, 5 ,6 ,7]},
            //     sheetName: 'Reporte Areas Sociales',
            //    title: 'reas Sociales'  },
            // {  extend : 'pdfHtml5',
            //     orientation: 'landscape',
            //    customize: function(doc) {
            //         doc.styles.tableBodyEven.alignment = 'center';
            //         doc.styles.tableBodyOdd.alignment = 'center';
            //    },
            //    exportOptions : {
            //         columns : [0, 1, 2, 3, 4, 5 ,6 ,7]
            //     },
            //    title: 'reas Sociales'
            // }
        ],
        initComplete: function () {


        },
        "order": [[ 0, "desc" ]],
        language : {
            'url': '/resources/js/spanish.json',
        },
        "pageLength": 50
    });
}



  startbutton.addEventListener('click', function(ev){
      takepicture();
    ev.preventDefault();
  }, false);



$(document).ajaxStart(function () {
});



$(document).ajaxStop(function () {
    $.Toast.hideToast();
});



function encender_camara() {

        var p = navigator.mediaDevices.getUserMedia(constraints);

        p.then(function(mediaStream) {
          var video = document.querySelector('video');
            try {
                video.srcObject = mediaStream;
            } catch (error) {

                video.src = window.URL.createObjectURL(mediaStream)
            }

        });

}


$('#new').click(function () {

    $('#nombre').val($('#pnombre').val())
    $('#show_img').attr('src', $('#pfoto').val());
    $('#row_video').show()
    $('#row_info').show()

    // Acceso a la webcam

    Promise.all([
        faceapi.nets.tinyFaceDetector.loadFromUri('/resources/plugins/face-api/models'),
        faceapi.nets.faceLandmark68Net.loadFromUri('/resources/plugins/face-api/models'),
        faceapi.nets.faceRecognitionNet.loadFromUri('/resources/plugins/face-api/models'),
        faceapi.nets.faceExpressionNet.loadFromUri('/resources/plugins/face-api/models'),
        faceapi.nets.ageGenderNet.loadFromUri('/resources/plugins/face-api/models'),
        faceapi.nets.ssdMobilenetv1.loadFromUri('/resources/plugins/face-api/models')
    ]).then(encender_camara)

    video.addEventListener('play', function(ev){

          var canvas = faceapi.createCanvasFromMedia(video)
          // document.body.append(canvas);
          var contador = 0;

          document.getElementById('body_video').appendChild(canvas);

            var displaySize = {width: video.width, height: video.height};
            faceapi.matchDimensions(canvas,displaySize);

            setInterval(async () =>{
                // const labeledFaceDescriptors = await loadLabeledImages();
                // const faceMatcher = new faceapi.FaceMatcher(labeledFaceDescriptors, 0.6);

                // var detections = await faceapi.detectAllFaces(video).withFaceLandmarks().withFaceDescriptors();
                // var resizeDetection =  faceapi.resizeResults(detections,displaySize);
                //
                // canvas.getContext('2d').clearRect(0,0, canvas.width,canvas.height);
                // faceapi.draw.drawDetections(canvas, resizeDetection)



                // const results = resizeDetection.map(d => faceMatcher.findBestMatch(d.descriptor))
                // // console.log(results)
                // results.forEach((result, i) => {
                //   const box = resizeDetection[i].detection.box
                //   const drawBox = new faceapi.draw.DrawBox(box, { label: result.toString() })
                //   drawBox.draw(canvas)
                //
                //   console.log(result.toString())
                //
                //     if (contador == 4){
                //         validar_cara(result.toString());
                //     }
                //
                //   contador = contador + 1;
                //   console.log(contador)
                //
                // })


                    var detections = await faceapi.detectAllFaces(video,new faceapi.TinyFaceDetectorOptions());
                    // console.log(detections)

                    var resizeDetection = faceapi.resizeResults(detections,displaySize);
                    canvas.getContext('2d').clearRect(0,0, canvas.width,canvas.height);
                    faceapi.draw.drawDetections(canvas,resizeDetection);
                    if (detections.length == 0 ){
                        console.log("no cara")
                    }else{
                        console.log("si cara")
                        if (contador == 1){
                            sacar_foto();
                        }
                        contador = contador + 1;

                    }

            }, 1000);

      }, false);


    function sacar_foto() {
         height = video.videoHeight / (video.videoWidth/width);
        canvasf.setAttribute('width', width);
        canvasf.setAttribute('height', height);
        streaming = true;
        canvasf.width = width;
        canvasf.height = height;
        canvasf.getContext('2d').drawImage(video, 0, 0, 250, 250);
        var dataf = canvasf.toDataURL('image/png');
        photo.setAttribute('src', dataf);

        validar_cara()



    }

    function loadLabeledImages() {
        const labels = [$('#pnombre').val()]

        return Promise.all(
            labels.map(async label => {
            const descriptions = []

            const img = await faceapi.fetchImage($('#pfoto').val())

            const fullFaceDescription  = await faceapi.detectSingleFace(img).withFaceLandmarks().withFaceDescriptor()

            // console.log("foto escaneada")

            descriptions.push(fullFaceDescription.descriptor)

          return new faceapi.LabeledFaceDescriptors(label, descriptions)
        })
        )
    }

    function validar_cara() {
        console.log("entro valida cara")

        var foto = document.getElementById('photo').getAttribute('src');
        // console.log(foto)
        obj = JSON.stringify({
            'fkpersona': $('#pid').val(),
            'foto': foto
        })
        // console.log("creo objeto")
        ajax_call_get('portal_asistencia_insert', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;

            if(self['respuesta']){
                // console.log("login true")

                swal(
                  'Marcacion Correcta.',
                  '.',
                  'success'
                )

                setTimeout(function () {
                    window.location = main_route
                }, 2000);

            }else{
                swal(
                  'Marcacion Invalida.',
                  'Al parecer no se reconocio el rostro',
                  'error'
                )
                setTimeout(function () {
                    window.location = main_route
                }, 2000);
            }

        })
    }

})


$('#new_coordenadas').click(function () {
    $('#nombre_coordenadas').val($('#pnombre_coordenadas').val())
    
        if ("geolocation" in navigator){ //check geolocation available
            //try to get user current location using getCurrentPosition() method
            navigator.geolocation.getCurrentPosition(function(position){
                    console.log("Found your location nLat : "+position.coords.latitude+" nLang :"+ position.coords.longitude);
                    localStorage.setItem('latitud',position.coords.latitude)
                    localStorage.setItem('longitud',position.coords.longitude)
                    console.log(localStorage.getItem("latitud"))
                    console.log(localStorage.getItem("longitud"))

                    $("#iframe").attr("src", "portal/asistencia/views/mapa.html")
            });
        }else{
            console.log("Browser doesn't support geolocation!");
        }
    

    verif_inputs('')
    validationInputSelects("form")
    $('#id_div_coordenadas').hide()
    $('#insert_coordenadas').show()
    $('#update_coordenadas').hide()
    validationInputSelects("form")
    $('#form_coordenadas').modal('show')
})

$('#new_foto').click(function () {


    $('#nombre').val($('#pnombre').val())
    $('#show_img').attr('src', $('#pfoto').val());
    $('#row_video').show()
    $('#row_info').show()

    // Acceso a la webcam

    Promise.all([
        faceapi.nets.tinyFaceDetector.loadFromUri('/resources/plugins/face-api/models'),
        faceapi.nets.faceLandmark68Net.loadFromUri('/resources/plugins/face-api/models'),
        faceapi.nets.faceRecognitionNet.loadFromUri('/resources/plugins/face-api/models'),
        faceapi.nets.faceExpressionNet.loadFromUri('/resources/plugins/face-api/models'),
        faceapi.nets.ageGenderNet.loadFromUri('/resources/plugins/face-api/models'),
        faceapi.nets.ssdMobilenetv1.loadFromUri('/resources/plugins/face-api/models')
    ]).then(encender_camara)

    video.addEventListener('play', function(ev){

          var canvas = faceapi.createCanvasFromMedia(video)
          // document.body.append(canvas);
          var contador = 0;

          document.getElementById('body_video').appendChild(canvas);

            var displaySize = {width: video.width, height: video.height};
            faceapi.matchDimensions(canvas,displaySize);

            setInterval(async () =>{
                const labeledFaceDescriptors = await loadLabeledImages();
                const faceMatcher = new faceapi.FaceMatcher(labeledFaceDescriptors, 0.6);

                var detections = await faceapi.detectAllFaces(video).withFaceLandmarks().withFaceDescriptors();
                var resizeDetection =  faceapi.resizeResults(detections,displaySize);

                canvas.getContext('2d').clearRect(0,0, canvas.width,canvas.height);
                faceapi.draw.drawDetections(canvas, resizeDetection)



                const results = resizeDetection.map(d => faceMatcher.findBestMatch(d.descriptor))
                // console.log(results)
                results.forEach((result, i) => {
                  const box = resizeDetection[i].detection.box
                  const drawBox = new faceapi.draw.DrawBox(box, { label: result.toString() })
                  drawBox.draw(canvas)

                  console.log(result.toString())

                    if (contador == 4){
                        validar_cara(result.toString());
                    }

                  contador = contador + 1;
                  console.log(contador)

                })


            }, 1000);

      }, false);


    function sacar_foto() {
         height = video.videoHeight / (video.videoWidth/width);
        canvasf.setAttribute('width', width);
        canvasf.setAttribute('height', height);
        streaming = true;
        canvasf.width = width;
        canvasf.height = height;
        canvasf.getContext('2d').drawImage(video, 0, 0, 250, 250);
        var dataf = canvasf.toDataURL('image/png');
        photo.setAttribute('src', dataf);

        validar_cara()



    }

    function loadLabeledImages() {
        const labels = [$('#pnombre').val()]

        return Promise.all(
            labels.map(async label => {
            const descriptions = []

            const img = await faceapi.fetchImage($('#pfoto').val())

            const fullFaceDescription  = await faceapi.detectSingleFace(img).withFaceLandmarks().withFaceDescriptor()

            // console.log("foto escaneada")

            descriptions.push(fullFaceDescription.descriptor)

          return new faceapi.LabeledFaceDescriptors(label, descriptions)
        })
        )
    }

    function validar_cara(resultado) {

        resultado = resultado.substr(0,7)

        if (resultado == 'unknown'){
            swal(
              'Marcacion Invalida.',
              'Al parecer no se reconocio el rostro vuelve a intentarlo',
              'error'
            )
            setTimeout(function () {
                window.location = main_route
            }, 2000);

        }else{

            objeto = JSON.stringify({
                'fkpersona': $('#pid').val()

            })
            ajax_call('portal_asistencia_update', {
                object: objeto,
                _xsrf: getCookie("_xsrf")
            }, null, function () {
                swal(
                  'Marcacion Correcta.',
                  '.',
                  'success'
                )

                setTimeout(function () {
                    window.location = main_route
                }, 2000);
            })

        }

    }


})


$('#insert').click(function () {
    notvalid = validationInputSelectsWithReturn("form");
    if (notvalid === false) {
        objeto = JSON.stringify({
            'nombre': $('#nombre').val(),
            'descripcion': $('#descripcion').val()
        })
        ajax_call('portal_asistencia_insert', {
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

$('#insert_coordenadas').click(function () {

        objeto = JSON.stringify({
            'fkpersona': $('#pid_coordenadas').val(),
            
            'latitud': localStorage.getItem("latitud"),
            'longitud':localStorage.getItem("longitud")

        })
        
            ajax_call('portal_coordenadas_insert', {
                object: objeto,
                    _xsrf: getCookie("_xsrf")
                }, null, function () {
                    setTimeout(function () {
                    window.location = main_route
                }, 2000);
            })
            $('#form_coordenadas').modal('hide')

})

$('#obtener_geolocalizacion').click(function () {
        if ("geolocation" in navigator){ //check geolocation available
            //try to get user current location using getCurrentPosition() method
            navigator.geolocation.getCurrentPosition(function(position){
                    console.log("Found your location nLat : "+position.coords.latitude+" nLang :"+ position.coords.longitude);
                    localStorage.setItem('latitud',position.coords.latitude)
                    localStorage.setItem('longitud',position.coords.longitude)
            });
        }else{
            console.log("Browser doesn't support geolocation!");
        }

})

$('#cargar_mapa').click(function () {
    $("#iframe").attr("src", "portal/asistencia/views/mapa.html")
})


function attach_edit() {
    $('.edit').click(function () {
        obj = JSON.stringify({
            'id': parseInt(JSON.parse($(this).attr('data-json')))
        })
        ajax_call_get('portal_asistencia_update', {
            _xsrf: getCookie("_xsrf"),
            object: obj
        }, function (response) {
            var self = response;
            $('#id').val(self.id)
            $('#nombre').val(self.nombre)
            $('#descripcion').val(self.descripcion)

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
    if (notvalid === false) {
        objeto = JSON.stringify({
            'id': parseInt($('#id').val()),
            'nombre': $('#nombre').val(),
            'descripcion': $('#descripcion').val()
        })
        ajax_call('portal_asistencia_update', {
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

// function attach_delete(idcb) {
//         id = idcb
//         enabled = false
//         swal({
//             title: "Â¿Desea dar de baja el tipo de asistencia?",
//             type: "warning",
//             showCancelButton: true,
//             confirmButtonColor: "#1565c0",
//             cancelButtonColor: "#F44336",
//             confirmButtonText: "Aceptar",
//             cancelButtonText: "Cancelar"
//         }).then(function () {
//             ajax_call('portal_asistencia_delete', {
//                 id: id,
//                 enabled: enabled,
//                 _xsrf: getCookie("_xsrf")
//             }, null, function () {
//                 setTimeout(function () {
//                     window.location = main_route
//                 }, 2000);
//             })
//         })
// }


$('.delete').click(function (e) {
    e.preventDefault()
    cb_delete = this
    b = $(this).prop('checked')
    if (!b) {
        cb_title = "¿Está seguro de que desea dar de baja el tipo de asistencia?"

    } else {
        cb_title = "¿Está seguro de que desea dar de alta el tipo de asistencia?"
    }
    swal({
        title: cb_title,
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#1565c0",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    }).then(function () {
        $(cb_delete).prop('checked', !$(cb_delete).is(':checked'))
        objeto = JSON.stringify({
            id: parseInt($(cb_delete).attr('data-id')),
            enabled: $(cb_delete).is(':checked')
        })
        ajax_call('portal_asistencia_delete', {
            object: objeto,
            _xsrf: getCookie("_xsrf")
        }, null, function () {
            setTimeout(function () {
                window.location = main_route
            }, 2000);
        })
        $('#form').modal('hide')
    })
})

validationKeyup("form");
validationSelectChange("form");