import os
import queue
import signal
import subprocess
import time
import atexit
from threading import Thread

import psutil
from flask import Flask, request

app = Flask(__name__)
print(os.getpid())

global child_pid, proc, running

proc = None
running = False
q = queue.Queue()


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


@app.post('/startparamter')
def startNuvoLedWithParameter():
    global proc, child_pid, running
    if running:
        return "failed to launch | another instance is running", 404
    running = True
    request_data = request.get_json()
    proc = subprocess.Popen(["java", "-jar", "nuvoled-1.0-SNAPSHOT-jar-with-dependencies.jar", "-py",
                             str(request_data["py"]), "-px",
                             str(request_data["px"]), "-br", str(request_data["brightness"]), "-r",
                             str(request_data["rotation"]), "-sn", str(request_data["screennumber"])],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    child_pid = proc.pid
    createStatusLoop()
    return "started", 200


@app.post('/start')
def startNuvoLed():
    global proc, child_pid, running
    running = True
    proc = subprocess.Popen(["java", "-jar", "nuvoled-1.0-SNAPSHOT-jar-with-dependencies.jar"], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    child_pid = proc.pid
    print(child_pid)
    createStatusLoop()
    return "started", 200


def statusLoop():
    while running:
        print("status:", proc.stdout.readline())
        line = proc.stdout.readline()
        q.put(line)


def createStatusLoop():
    print("start Status:")
    thread = Thread(target=statusLoop)
    thread.start()


@app.get('/status')
def getAllStatus():
    if (q.empty()):
        return "nothing in que", 200
    status = q.get(timeout=1)
    return status, 200


@app.get('/statusonoff')
def getStatus():
    if running:
        return "online", 404
    else:
        return "offline", 200


@app.post('/stop')
def stopNuvoLed():
    global proc, running
    running = False
    print("terminate")
    kills(child_pid)
    (output, error) = proc.communicate()
    s = error + output
    proc = None

    return str(s), 200
