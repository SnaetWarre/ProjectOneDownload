'use strict;'

const init = function () {
    const sidebarbutton = document.getElementById('sidebarbutton')
    sidebarbutton.addEventListener('click', function () {
        window.location.href = 'sidebar.html';
    });

    const button3 = document.querySelector('.js-shutdown');

    button3.addEventListener('click', function () {
        console.log('Shutdown of RaspberryPi');
        socketio.emit('F2B_STOP_RASPBERRY');
    });

    // MODAL TO SHUTDOWN RASPBERRYPI
    // Get the modal
    var modal = document.getElementById('ModalStopPi');

    // Get the button that opens the modal
    var btn = document.getElementById('BtnStopPi');

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName('ClosePi')[0];

    // When the user clicks on the button, open the modal
    btn.onclick = function () {
        modal.style.display = 'block';
    };

    // When the user clicks on <span> (x), close the modal
    span.onclick = function () {
        modal.style.display = 'none';
    };

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    };

}

document.addEventListener('DOMContentLoaded', init);