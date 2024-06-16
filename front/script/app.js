const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);

const listenToUI = function () { };

let chartBPM, chartTemp, chartAir;

let bpmData,
  tempData,
  airData = [];
let chartTime = [];

const listenToSocket = function () {
  socketio.on('connect', function () {
    console.log('verbonden met socket webserver');
  });

  socketio.on('F2B_UPDATE_TITLE_SUCCES', function (data) {
    console.log('title Updated');
    const succesElement = document.getElementById('succesmessage');

    succesElement.innerHTML = 'Title updated succesfully';
    succesElement.classList.add('show');
  });

  socketio.on('B2F_AVERAGE_BPM', function (data) {
    document.querySelector(
      '.js-average-bpm'
    ).innerHTML = `The average bpm: ${data.AVERAGE_BPM}`;
    bpmData.push(data.AVERAGE_BPM);
    document.getElementById(
      'bpm-overlay'
    ).style.display = "none";
    document.querySelector(".js-chartbpm").style.filter = "blur(0px)";
    chartTime.push(new Date().toLocaleTimeString());
    chartBPM.updateSeries([
      {
        name: 'BPM',
        data: bpmData,
      },
    ]);
  });

  socketio.on('B2F_TEMPERATURE', function (data) {
    document.querySelector(
      '.js-temperature'
    ).innerHTML = `Temperature: ${data.temperature} °C`;
    tempData.push(data.temperature);
    chartTime.push(new Date().toLocaleTimeString());
    chartTemp.updateSeries([
      {
        name: 'Temperature',
        data: tempData,
      },
    ]);
  });

  socketio.on('B2F_QUALITY', function (data) {
    document.querySelector(
      '.js-quality'
    ).innerHTML = `Quality: ${data.quality}`;
    airData.push(data.quality);
    chartTime.push(new Date().toLocaleTimeString());
    chartAir.updateSeries([
      {
        name: 'Air Quality',
        data: airData,
      },
    ]);
  });
};

const showChartsBpm = function (data, time) {
  bpmData = data;
  chartTime = time;

  let options = {
    series: [
      {
        name: 'BPM',
        data: data,
      },
    ],
    chart: {
      height: 200,
      type: 'line',
      zoom: {
        enabled: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      curve: 'smooth',
    },
    title: {
      text: 'The Beats Per Minute (BPM)',
      align: 'center',
    },
    grid: {
      row: {
        colors: ['#EEF1F5', 'transparent'], // takes an array which will be repeated on columns
        opacity: 0.5,
      },
    },
    xaxis: {
      categories: time,
      labels: {
        show: false,
      },
    },
  };

  chartBPM = new ApexCharts(document.querySelector('.js-chartbpm'), options);
  chartBPM.render();
};

const showChartsTemp = function (data, time) {
  tempData = data;
  chartTime = time;

  let options = {
    series: [
      {
        name: 'Temperature',
        data: data,
      },
    ],
    chart: {
      height: 200,
      type: 'line',
      zoom: {
        enabled: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      curve: 'smooth',
    },
    title: {
      text: 'The Temperature in °C',
      align: 'center',
    },
    grid: {
      row: {
        colors: ['#EEF1F5', 'transparent'], // takes an array which will be repeated on columns
        opacity: 0.5,
      },
    },
    xaxis: {
      categories: time,
      labels: {
        show: false,
      },
    },
  };

  chartTemp = new ApexCharts(document.querySelector('.js-charttemp'), options);
  chartTemp.render();
};

const showChartsAir = function (data, time) {
  airData = data;
  chartTime = time;

  let options = {
    series: [
      {
        name: 'Air Quality',
        data: data,
      },
    ],
    chart: {
      height: 200,
      type: 'line',
      zoom: {
        enabled: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      curve: 'smooth',
    },
    title: {
      text: 'The Air Quality',
      align: 'center',
    },
    grid: {
      row: {
        colors: ['#EEF1F5', 'transparent'], // takes an array which will be repeated on columns
        opacity: 0.5,
      },
    },
    xaxis: {
      categories: time,
      labels: {
        show: false,
      },
    },
  };

  chartAir = new ApexCharts(document.querySelector('.js-chartair'), options);
  chartAir.render();
};

const ListenToButtons = function () {
  const startsessionBtn = document.querySelector('.js-startsession');
  const button2 = document.querySelector('.js-stopsession');
  const button3 = document.querySelector('.js-shutdown');
  const button4 = document.querySelector('.js-updatetitle');
  const input = document.getElementById('userInputTitle');
  const sidebarbutton = document.getElementById('sidebarbutton')

  startsessionBtn.addEventListener('click', function () {
    console.log('Started session');
    const username = document.cookie.split('=')[1];
    const data = { username: username };
    fetch(`http://${lanIP}/api/v1/start/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((result) => {
        console.log('Started session');
        document.querySelector(
          '.js-average-bpm'
        ).innerHTML = `Loading BPM <span id="dots"></span>`;
        loadingDots()

        document.getElementById(
          'bpm-overlay'
        ).style.display = "flex";

        document.querySelector(".js-chartbpm").style.filter = "blur(2px)";
      })
      .catch((error) => {
        console.error('Error starting session:', error);
      });
  });

  button2.addEventListener('click', function () {
    console.log('Stopped session');
    socketio.emit('F2B_STOP_SESSION');
  });

  button3.addEventListener('click', function () {
    console.log('Shutdown of RaspberryPi');
    socketio.emit('F2B_STOP_RASPBERRY');
  });

  button4.addEventListener('click', function () {
    console.log('Updating Title');
    const inputtitle = input.value;
    socketio.emit('F2B_UPDATE_TITLE', inputtitle);

    // modal2.style.display = 'none';
  });

  sidebarbutton.addEventListener('click', function () {
    window.location.href = 'sidebar.html';
  });
};

const loadingDots = function () {
  const dots = document.getElementById("dots")
  dots.innerHTML = '.'
  setInterval(() => {
    if (dots.innerHTML.length < 3) {
      dots.innerHTML += '.'
    } else {
      dots.innerHTML = ''
    }
  }, 250);
}

const init = function () {
  console.info('DOM geladen');

  listenToUI();
  listenToSocket();
  ListenToButtons();

  // Initialize charts with empty data
  showChartsBpm([], []);
  showChartsTemp([], []);
  showChartsAir([], []);

  const usernameElement = document.getElementById('username');
  usernameElement.innerText = document.cookie.split('=')[1];

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

  //MODAL TO GIVE A TITLE TO A SESSION
  // MODAL TO GIVE A TITLE TO A SESSION
var modal2 = document.getElementById('ModalTitel');

// Get the button that opens the modal
var btn2 = document.getElementById('BtnStopSession');

// Get the <span> element that closes the modal
var span2 = document.getElementsByClassName('CloseTitel')[0];

// Get the input field
var inputField = document.getElementById('userInputTitle');

// When the user clicks on the button, open the modal and focus the input field
btn2.onclick = function () {
    modal2.style.display = 'block';
    inputField.focus();  // Focus the input field
};

// When the user clicks on <span> (x), close the modal
span2.onclick = function () {
    modal2.style.display = 'none';
};

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == modal2) {
        modal2.style.display = 'none';
    }
};

};

document.addEventListener('DOMContentLoaded', init);