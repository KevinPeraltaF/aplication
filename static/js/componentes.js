function mensaje_basico(mensaje) {
    Swal.fire(mensaje)
}

function mensaje_con_titulo(titulo_principal, titulo_secundario, icono) {
    Swal.fire(
        titulo_principal,
        titulo_secundario,
        icono
    )
}


function mensaje_success(titulo) {
    Swal.fire({
        position: 'top-end',
        icon: 'success',
        title: titulo,
        showConfirmButton: false,
        timer: 1500
    })
}

function mensaje_error(mensaje, titulo) {
    Swal.fire({
        icon: 'error',
        title: titulo,
        text: mensaje,

    })
}

function mensaje_alerta(mensaje, titulo) {
    Swal.fire({
        icon: 'error',
        title: titulo,
        text: mensaje,

    })
}






