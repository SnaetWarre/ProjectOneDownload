const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);

const listenToUI = function () { };



const listenToSocket = function () {
  socketio.on('connect', function () {
    console.log('verbonden met socket webserver');
  });


}

const ListenToButtons = function () {
  
  const shutdownbutton = document.querySelector('.js-shutdown');

  

  shutdownbutton.addEventListener('click', function () {
    console.log('Shutdown of RaspberryPi');
    socketio.emit('F2B_STOP_RASPBERRY');
  });

  
};



const init = function () {
  console.info('DOM geladen');
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

  
};

document.addEventListener('DOMContentLoaded', init);