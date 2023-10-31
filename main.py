import os
import signal
import subprocess
import time

from flask import Flask, request

app = Flask(__name__)
print(os.getpid())

@app.get('/version')
def getJavaVersion():
    print("version")
    a = subprocess.run(['java', '--version'], capture_output=True, shell=True)
    print(a.stdout)
    return str(a.stdout), 200


@app.post('/start')
def startNuvoLed():
    print("start")
    p = subprocess.Popen(['java', '-jar', 'nuvoled-1.0-SNAPSHOT-jar-with-dependencies.jar'],
                         stdout=subprocess.PIPE,
                         shell=True)
    time.sleep(2)
    print(p.pid)
    os.kill(p.pid, signal.CTRL_C_EVENT)
    return "start", 200


@app.post('/stop')
def stopNuvoLed():
    #p.send_signal(signal.CTRL_C_EVENT)
    return "stop", 200
