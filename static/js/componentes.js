function mensaje_basico() {
    Swal.fire('Any fool can use a computer')
}

function mensaje_con_titulo(titulo_principal, titulo_secundario,icono) {
    Swal.fire(
        titulo_principal,
        titulo_secundario,
        icono
    )
}


function dialogo_con_tres_botones(titulo) {
    Swal.fire({
        title: titulo,
        showDenyButton: true,
        showCancelButton: true,
        confirmButtonText: 'Save',
        denyButtonText: `Don't save`,
    }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
            Swal.fire('Saved!', '', 'success')
        } else if (result.isDenied) {
            Swal.fire('Changes are not saved', '', 'info')
        }
    })
}

function mensaje_con_posicion(titulo,icono) {
    Swal.fire({
        position: 'top-end',
        icon:icono,
        title: titulo,
        showConfirmButton: false,
        timer: 1500
    })
}

function mensaje_error(mensaje,titulo) {
    Swal.fire({
        icon: 'error',
        title: titulo,
        text: mensaje,

    })
}

function dialogo_accion_si_no(titulo,icono) {
    Swal.fire({
        position: 'top-end',
        icon: icono,
        title: titulo,
        showConfirmButton: false,
        timer: 1500
    })
}