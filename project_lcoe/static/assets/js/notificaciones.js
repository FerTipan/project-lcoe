function mostrarNotificaciones(mensajes) {
  const notyf = new Notyf({
    duration: 3000,
    position: { x: 'right', y: 'top' },
    dismissible: true
  });

  mensajes.forEach(mensaje => {
    if (mensaje.tipo.includes("success")) {
      notyf.success(mensaje.texto);
    } else if (mensaje.tipo.includes("error")) {
      notyf.error(mensaje.texto);
    } else {
      notyf.open({ type: 'info', message: mensaje.texto });
    }
  });
}

// Confirmación de eliminación
function confirmarEliminacion(pk) {
  Swal.fire({
    title: '¿Confirmar eliminación?',
    text: 'Está seguro de eliminar esta información',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Eliminar',
    cancelButtonText: 'Cancelar',
    reverseButtons: true,
    focusCancel: true
  }).then((result) => {
    if (result.isConfirmed) {
      document.getElementById('form-eliminar-' + pk).submit();
    }
  });
}
