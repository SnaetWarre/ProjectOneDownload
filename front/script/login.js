const lanIP = `${window.location.hostname}:5000`;

const loginSuccess = function (resp) {
    console.log(resp)
    document.cookie = `username=${resp.Username}`;


    window.location.href = 'home.html';
};

const loginFailed = function (resp) {
    const errorElement = document.getElementById("error")

    errorElement.innerHTML = "User not found"
    errorElement.classList.add("show")
}

const registerSuccess = function (resp) {
    document.cookie = `username=${resp.username}`;

    window.location.href = 'home.html';
}

const registerFailed = function (resp) {
    const errorElement = document.getElementById("error")

    errorElement.innerHTML = "User already exists"
    errorElement.classList.add("show")
}

const init = function () {
    const formlogin = document.getElementById('form');

    formlogin.addEventListener('submit', (e) => {
        e.preventDefault();

        if (e.submitter.innerHTML == "Register") {
            // Get the values from the form inputs
            const username = document.getElementById('username').value;
            const dob = document.getElementById('dob').value;
            const bpm = document.getElementById('bpm').value;

            // create socketio message to send that data to the backend server
            const data = JSON.stringify({
                username,
                dob,
                bpm
            });

            // Send the data to the backend server
            handleData(`http://${lanIP}/api/v1/user/`, registerSuccess, registerFailed, 'POST', data);
        } else {
            // Get the values from the form inputs

            const username = document.getElementById('username').value;
            const bpm = document.getElementById('bpm').value;

            const bodylogin = JSON.stringify({
                username, bpm
            })

            handleData(`http://${lanIP}/api/v1/user/checkexisting/`, loginSuccess, loginFailed, 'POST', bodylogin);
        }
    });
};



document.addEventListener('DOMContentLoaded', init);