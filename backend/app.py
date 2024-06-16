import threading
import time
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# TODO: GPIO
import time
import numpy as np
from collections import deque
from scipy.signal import find_peaks
from testingcomponents.max30102 import MAX30102
from testingcomponents.airquality import MCP
from testingcomponents.LCD import LCD
import subprocess
import RPi.GPIO as GPIO

endpoint = "/api/v1"
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisismyveryverysecretkeyformyflask'
# ping interval forces rapid B2F communication
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent', ping_interval=0.5)
CORS(app)

global UserID
UserID = 0

global status
status = 0

global sessionID
sessionID = 0

global bpm 
bpm = 0

# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')

bpm = 0
def read_heartbeat():
    fs = 100  # Sampling frequency (Hz)
    max_sensor = MAX30102()
    ir_data_deque = deque(maxlen=1000)  # Store enough data for analysis
    while status == 1:
        ir_data, red_data = max_sensor.read_fifo()
        if ir_data:
            ir_data_deque.extend(ir_data)

            # Calculate BPM every second
            if len(ir_data_deque) >= 100:
                filtered_ir = max_sensor.bandpass_filter(list(ir_data_deque), lowcut=0.5, highcut=5.0, fs=fs, order=3)
                peaks, _ = find_peaks(filtered_ir, distance=fs/3)  # minimum 1/3 seconde per peak?
                bpm_values = max_sensor.calculate_bpm(peaks, fs=fs)
                if len(bpm_values) > 0:
                    average_bpm = np.mean(bpm_values)
                    # print(f"Average BPM: {average_bpm:.2f}")
                    global bpm
                    bpm = average_bpm.round(2)
                    socketio.emit('B2F_AVERAGE_BPM', {'AVERAGE_BPM': bpm})
                    DataRepository.insert_values_history(1,1,sessionID, bpm, "heartbeat")
        time.sleep(0.5)

@app.route(endpoint + '/history/heartbeat/', methods=['GET','POST'])
def add_heart_rate_value():
    if request.method == 'POST':
        payload = DataRepository.json_or_formdata(request)
        new_id = DataRepository.insert_values_history(payload[1], payload[1], payload[sessionID], payload[bpm], payload["heartbeat values"])
        if (new_id > 0):
            return jsonify({'success': True}), 200
        else:
            return jsonify(boodschap="Something went wrong when trying to add this to the database (History table)"), 404
    
    elif request.method == 'GET':
        data = DataRepository.read_values_bpm()
        return jsonify(data), 200

temp = 0
def read_temperature():
    directory_path = "/sys/bus/w1/devices/28-00000de601b0/w1_slave"
    while status == 1:
        with open(directory_path, "r") as file:
            content = file.read()
            temp_string = content.split("t=")[1]
            temp = int(temp_string) / 1000
            socketio.emit('B2F_TEMPERATURE', {'temperature': temp})
            DataRepository.insert_values_history(2,2,sessionID, temp, "Temperatur values")
        time.sleep(0.5)

@app.route(endpoint + '/history/temperature/', methods=['GET','POST'])
def add_temperature_value():
    if request.method == 'POST':
        payload = DataRepository.json_or_formdata(request)
        new_id = DataRepository.insert_values_history(payload[2], payload[2], payload[sessionID], payload[temp], payload["Temperature values"])
        if (new_id > 0):
            return jsonify({'success': True}), 200
        else:
            return jsonify(boodschap="Something went wrong when trying to add this to the database (History table)"), 404

    elif request.method == 'GET':
        data = DataRepository.read_values_temp()
        return jsonify(data), 200

data = 0
def read_airquality():
    mcp = MCP()
    channel = 0
    while status == 1:
        data = mcp.read_channel(channel)
        # print(data)
        # voltage = mcp.convert_to_voltage(data)
        # print(f"Channel {channel} \n voltage: {voltage}V \n data: {data} ")
        socketio.emit('B2F_QUALITY', {'quality': data})
        DataRepository.insert_values_history(3, 3, sessionID, data,"Airquality values")
        time.sleep(0.5)

@app.route(endpoint + '/history/airquality/', methods=['GET','POST'])
def add_airquality_value():
    if request.method == 'POST':
        payload = DataRepository.json_or_formdata(request)
        new_id = DataRepository.insert_values_history(payload[3], payload[3], payload[sessionID], payload[data], payload["Airquality values"])
        if (new_id > 0):
            return jsonify({'success': True}), 200
        else:
            return jsonify(boodschap="Something went wrong when trying to add this to the database (History table)"), 404

    elif request.method == 'GET':
        data = DataRepository.read_values_air()
        return jsonify(data), 200


@app.route(endpoint + '/history/<sessionid>/bpm/', methods=['GET'])
def get_bpm_by_id(sessionid):
    data = DataRepository.read_bpm_by_id(sessionid)
    return jsonify(data), 200

@app.route(endpoint + '/history/<sessionid>/temp/', methods=['GET'])
def read_temp_by_id(sessionid):
    data = DataRepository.read_temp_by_id(sessionid)
    return jsonify(data), 200

@app.route(endpoint + '/history/<sessionid>/air/', methods=['GET'])
def read_air_by_id(sessionid):
    data = DataRepository.read_air_by_id(sessionid)
    return jsonify(data), 200

@app.route(endpoint + '/history/user/<username>/sessions/', methods=['GET'])
def get_all_sessionid(username):
    data = DataRepository.get_all_sessions(username)
    return jsonify(data), 200

@app.route(endpoint + '/user/' , methods=['POST'])
def make_user():
    if request.method == 'POST':
        payload = DataRepository.json_or_formdata(request)
        username = payload.get('username')

        userdata = DataRepository.check_user(username)
        if userdata != None:
            return jsonify({'success': False}), 403
        dob = payload.get('dob')
        maxbpmdb = payload.get('bpm')
        new_id = DataRepository.create_user(username, dob, maxbpmdb)
        # print(new_id)
        if (new_id > 0):
            return jsonify({ "username": username }), 200
        else:
            return jsonify(boodschap="Something went wrong when trying to add this to the database (user)"), 404

@app.route(endpoint + '/user/checkexisting/', methods=['POST'])
def check_user():
    if request.method == 'POST':
        payload = DataRepository.json_or_formdata(request)
        username = payload.get('username')
        data = DataRepository.check_user(username)
        if data == None:
            return jsonify({'success': False}), 404
        
        maxbpmdb = payload.get('bpm')
        DataRepository.update_user_bpm(username, maxbpmdb)
        return jsonify(data), 200

GPIO.setmode(GPIO.BCM)
lcd = LCD()
ip_addresses = []

def get_wlan0_ip_address():
    """
    Retrieves the IPv4 address assigned to the wlan0 interface.
    """
    try:
        ip_output = subprocess.check_output(["ip", "-4", "addr", "show", "wlan0"]).decode("utf-8")
        for line in ip_output.split("\n"):
            if "inet" in line:
                ip_address = line.split()[1].split("/")[0]
                return ip_address
    except subprocess.CalledProcessError:
        return None

def display_everything():
    """
    Continuously checks for the wlan0 IP address and updates the LCD display.
    """
    max_attempts = 100
    attempts = 0
    while attempts < max_attempts:
        wlan0_ip_address = get_wlan0_ip_address()
        if wlan0_ip_address:
            lcd.clear_display()
            lcd.write_message("IP Address:", 1)
            lcd.write_message(wlan0_ip_address, 2)
            break
        else:
            lcd.clear_display()
            lcd.write_message("Fetching IP...", 1)
            time.sleep(1)  
        attempts += 1

def motormodule(maxbpmdb):
    print("motormodule is gestart")
    GPIO.setup(16, GPIO.OUT)
    global status
    global bpm
    maxbpmdbint = int(maxbpmdb)
    while status == 1:
        if bpm > maxbpmdbint:
            # print(bpm)
            GPIO.output(16, GPIO.HIGH)                      
            time.sleep(0.5)
            GPIO.output(16, GPIO.LOW)
            time.sleep(0.5)
        else:
            GPIO.output(16, GPIO.LOW)
            time.sleep(0.5)


BUZZER_PIN = 26
GPIO.setup(BUZZER_PIN, GPIO.OUT)
global buzzer
buzzer = GPIO.PWM(BUZZER_PIN, 440)  # 440 Hz is a common frequency for a warning sound

def buzzermodule(maxbpmdb):
    print("buzzermodule is gestart")
    global status
    global bpm    
    maxbpmdbint = int(maxbpmdb)
    while status == 1:
        print(f"maxbpmdb: {maxbpmdbint}")
        print(f"bpm: {bpm}")
        if bpm > maxbpmdbint:
            print(f"maxbpmdb: {maxbpmdb}")
            print(f"bpm: {bpm}")
            warning_sound(maxbpmdb)
        else:
            buzzer.stop()
            time.sleep(0.5)

            

def warning_sound(maxbpmdb):
    """
    Play a warning sound with the passive buzzer.
    """
    global status
    frequencies = [440, 660, 550]  # List of frequencies to alternate between
    while status == 1:
        global bpm
        maxbpmdbint = int(maxbpmdb)
        if bpm > maxbpmdbint:
            for frequency in frequencies:
                buzzer.ChangeFrequency(frequency)
                buzzer.start(50)  # 50% duty cycle to make the sound audible
                time.sleep(0.4)
                buzzer.stop()
                time.sleep(0.2)



#### physical way (actual button)
SHUTDOWNBUTTON = 24
GPIO.setup(SHUTDOWNBUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def shutdownbuttonphy(channel):
    print("Shutdown button pressed on raspberry pi")
    subprocess.call(['sudo', 'shutdown', 'now'])

GPIO.add_event_detect(SHUTDOWNBUTTON, GPIO.FALLING, callback=shutdownbuttonphy, bouncetime=3000)

#### website button (button on website)

@socketio.on('F2B_STOP_RASPBERRY')
def shutdownbuttonweb():
    print("Shutdown button pressed on website")
    subprocess.call(['sudo', 'shutdown', 'now'])


@socketio.on('F2B_UPDATE_TITLE')
def updating_title(title):
    print('updating title from last session')
    print(title)
    DataRepository.update_title(title)
    socketio.emit('F2B_UPDATE_TITLE_SUCCES', title)




def webserver():
    print("webserver started")
    socketio.run(app, debug=False, host='0.0.0.0')

def start_webserver_lcd ():
    threading.Thread(target=webserver, daemon=True).start()
    threading.Thread(target=display_everything, daemon=True).start()
    print("Webserver and lcd started")

def start_hardware(maxbpmdb):
    threading.Thread(target=read_heartbeat, daemon=True).start()
    threading.Thread(target=read_temperature, daemon=True).start()
    threading.Thread(target=read_airquality, daemon=True).start()
    threading.Thread(target=motormodule, args=({ maxbpmdb }), daemon=True).start()
    threading.Thread(target=buzzermodule, args=({ maxbpmdb }), daemon=True).start()
    print("hardware threads started")

@app.route(endpoint + '/start/' , methods=['POST'])
def start_hardware_on_socket():
    payload = DataRepository.json_or_formdata(request)
    username = payload.get('username')

    print('start hardware')
    global status
    status = 1
    starttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # print(starttime)

    # print("username" + username)
    user = DataRepository.check_user(username)
    # print(user['UserID'])

    global UserID
    UserID = user['UserID']

    global sessionID
    sessionID = DataRepository.start_session(UserID , starttime)
    
    

    start_hardware(user['Maxbpm'])
    # print("SessionID: ")
    # print(sessionID)

    return jsonify({'success': True}), 200

    
@socketio.on('F2B_STOP_SESSION')
def stop_hardware():
    print('stop hardware')
    global status 
    status = 0
    endtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    DataRepository.end_session(endtime)

if __name__ == '__main__':
    try:
        print("**** Starting APP ****")
        start_webserver_lcd()
        while True:
            time.sleep(0.2)
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')
        lcd.clear_display()
        GPIO.cleanup()
    finally:
        print("finished")


