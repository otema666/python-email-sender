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
