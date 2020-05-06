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