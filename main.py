import os
import signal
import subprocess
import time
import atexit

import psutil
from flask import Flask, request

app = Flask(__name__)
print(os.getpid())

global child_pid, proc

proc = None


def kills(pid):
    '''Kills all process'''
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        child.kill()
    parent.kill()


@app.get('/version')
def getJavaVersion():
    print("version")
    a = subprocess.run(['java', '--version'], capture_output=True, shell=True)
    print(a.stdout)
    return str(a.stdout), 200


@app.post('/start')
def startNuvoLed():
    global proc, child_pid
    proc = subprocess.Popen(["java", "-jar", "nuvoled-1.0-SNAPSHOT-jar-with-dependencies.jar"], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    child_pid = proc.pid
    print(child_pid)

    (output, error) = proc.communicate()
    s = error + output
    return str(s), 200

    # return "started", 200


@app.get('/status')  # ------- seperate loop --------------
def getStatus():
    if proc is None:
        return "offline", 200
    (output, error) = proc.communicate()
    s = error + output
    return str(s), 200


@app.post('/stop')
def stopNuvoLed():
    print("terminate")
    kills(child_pid)
    (output, error) = proc.communicate()
    s = error + output
    return str(s), 200
