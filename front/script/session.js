const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);

let sessionid = 0;

let chartBPM, chartTemp, chartAir;

let sessionidhtml;

let bpmData, tempData, airData = [];
let chartTime = [];

const showChartsBpm = function (data, time) {
    bpmData = data;
    chartTime = time;

    if (chartBPM) {
        chartBPM.destroy();
    }

    let options = {
        series: [
            {
                name: 'BPM',
                data: data,
            },
        ],
        chart: {
            height: 400,
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
                show: true,
            },
        },
    };

    chartBPM = new ApexCharts(document.querySelector('.js-chartbpmsession'), options);
    chartBPM.render();
};

const showChartsTemp = function (data, time) {
    tempData = data;
    chartTime = time;

    if (chartTemp) {
        chartTemp.destroy();
    }

    let options = {
        series: [
            {
                name: 'Temperature',
                data: data,
            },
        ],
        chart: {
            height: 400,
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
                show: true,
            },
        },
    };

    chartTemp = new ApexCharts(document.querySelector('.js-charttempsession'), options);
    chartTemp.render();
};

const showChartsAir = function (data, time) {
    airData = data;
    chartTime = time;

    if (chartAir) {
        chartAir.destroy();
    }

    let options = {
        series: [
            {
                name: 'Air Quality',
                data: data,
            },
        ],
        chart: {
            height: 400,
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
                show: true,
            },
        },
    };

    chartAir = new ApexCharts(document.querySelector('.js-chartairsession'), options);
    chartAir.render();
};

const fetchBpm = function (data) {
    let values = data.map((item) => {
        return item.Value;
    });

    let times = data.map((item) => {
        return new Date(item.ActionDate).toLocaleTimeString();
    });

    showChartsBpm(values, times);
};

const fetchTemp = function (data) {
    let values = data.map((item) => {
        return item.Value;
    });

    let times = data.map((item) => {
        return new Date(item.ActionDate).toLocaleTimeString();
    });

    showChartsTemp(values, times);
};

const fetchAir = function (data) {
    let values = data.map((item) => {
        return item.Value;
    });

    let times = data.map((item) => {
        return new Date(item.ActionDate).toLocaleTimeString();
    });

    showChartsAir(values, times);
};

const showSessionID = function (data) {
    for (let i = 0; i < data.length; i++) {
        console.log(data[i].SessionID);

        sessionidhtml = document.querySelector('.js-sessionid');

        let str = `
            <option value="${data[i].SessionID}">${data[i].SessionID} ${data[i].Titel}</option>
        `;

        sessionidhtml.innerHTML += str;
    }
};

const getSessionId = function (data) {
    console.log(data);
    showSessionID(data);
};

const username = document.cookie.split('=')[1];

handleData(`http://${lanIP}/api/v1/history/user/${username}/sessions/`, getSessionId);

const init = function () {
    console.log('domcontentloaded');
    document.querySelector('.js-sessionid').addEventListener('change', function () {
        sessionid = this.value;
        console.log('Selected session ID:', sessionid);

        handleData(`http://${lanIP}/api/v1/history/${sessionid}/bpm/`, fetchBpm);
        handleData(`http://${lanIP}/api/v1/history/${sessionid}/temp/`, fetchTemp);
        handleData(`http://${lanIP}/api/v1/history/${sessionid}/air/`, fetchAir);
    });

    const usernameElement = document.getElementById('username');
    usernameElement.innerText = document.cookie.split('=')[1];

    const button3 = document.querySelector('.js-shutdown');

    button3.addEventListener('click', function () {
        console.log('Shutdown of RaspberryPi');
        socketio.emit('F2B_STOP_RASPBERRY');
    });

    const sidebarbutton = document.getElementById('sidebarbutton')
    sidebarbutton.addEventListener('click', function () {
        window.location.href = 'sidebar.html';
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
};

document.addEventListener('DOMContentLoaded', init);
