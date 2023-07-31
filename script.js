document.getElementById("saveButton").addEventListener("click", function() {
    
    const recipient = document.getElementById("recipient").value;
    const subject = document.getElementById("subject").value;
    const message = document.getElementById("message").value;
    const data = {
        recipient: recipient,
        subject: subject,
        message: message
    };

    // Realizar la solicitud POST al servidor local en la ruta '/save_email'
    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://localhost:8000/save_email', true); // Actualizar la ruta a '/save_email'
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                console.log(response); // Puedes manejar la respuesta del servidor aquí
            } else {
                console.error('Error al enviar la solicitud:', xhr.status, xhr.statusText);
            }
        }
    };
    xhr.send(JSON.stringify(data));
});

function show_msg() {
  // Deshabilitar el botón al hacer clic
  document.getElementById("saveButton").disabled = true;
  document.getElementById("saveButton").style.cursor = "not-allowed";

  // Iniciar el contador
  let count = 30;
  const interval = setInterval(function () {
    count--;
    if (count >= 0) {
      // Actualizar el texto del botón con el contador descendente
      document.getElementById("saveButton").innerText = `Enviar (${count})`;
    } else {
      // Habilitar el botón nuevamente después de 30 segundos
      document.getElementById("saveButton").disabled = false;
      document.getElementById("saveButton").style.cursor = "pointer";
      document.getElementById("saveButton").innerText = "Enviar";
      clearInterval(interval);
    }
  }, 1000); // 1000ms = 1 segundo

  const messageDiv = document.getElementById("messageDiv");
  messageDiv.textContent = "Mensaje enviado con éxito";
  messageDiv.classList.add("show");

  setTimeout(function() {
      messageDiv.classList.remove("show");
  }, 3000);
}
