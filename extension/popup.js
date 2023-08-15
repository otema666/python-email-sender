const sendButton = document.getElementById('sendButton');
const resultMessage = document.getElementById('resultMessage');
const emailForm = document.getElementById('emailForm');
const toggleDarkModeButton = document.getElementById('toggleDarkMode');

toggleDarkModeButton.addEventListener('click', () => {
  document.body.classList.toggle('dark-mode');
});

sendButton.addEventListener('click', () => {
  // Tu código para enviar el correo electrónico aquí
  startLoadingAnimation();
  setTimeout(function() {
    stopLoadingAnimation();
  }, 1800);
  

});

document.getElementById("sendButton").addEventListener("click", function() {
    const address = document.getElementById("address").value;
    const subject = document.getElementById("subject").value;
    const message = document.getElementById("message").value;
    const data = {
        address: address,
        subject: subject,
        message: message
    };

    // Realizar la solicitud POST al servidor local en la ruta '/save_email'
    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://localhost:5000/save_email', true); // Actualizar la ruta a '/save_email'
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
})



function startLoadingAnimation() {
    document.getElementById("loader-container").classList.remove("hidden");
    // Iniciar la animación de la barra de carga
    document.getElementById("loader").style.animation = "loading 1.8s ease-in-out forwards, change-color 1.8s ease-in-out forwards";
    //resultMessage.textContent = 'Email sent successfully.';
    //stopLoadingAnimation();
}
  
function stopLoadingAnimation() {

document.getElementById("loader-container").classList.add("hidden");
resultMessage.textContent = 'Email sent successfully.';
setTimeout(function() {
    resultMessage.textContent = '';
  }, 1800);


// Reiniciar la animación de la barra de carga
document.getElementById("loader").style.animation = "none";
document.getElementById("loader").offsetHeight;
document.getElementById("loader").style.animation = "loading 1.8s ease-in-out forwards";
}
  