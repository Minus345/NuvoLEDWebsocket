import logging
import os
import queue
import subprocess
import sys
from threading import Thread

import psutil
from flask import Blueprint, request

from flaskr.helper import findNuvoIp

global child_pid, proc, running, q, chromeId, runningChrome

#logging.basicConfig(filename='flaskr.log', encoding='utf-8', level=logging.DEBUG)

# < 3.9
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('flaskr.log', 'w', 'utf-8')
root_logger.addHandler(handler)

bp = Blueprint("main", __name__, url_prefix="/main")
proc = None
running = False
runningChrome = False
q = queue.Queue()
print(os.getpid())

def kills(pid):
    '''Kills all process'''
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        child.kill()
    parent.kill()

@bp.get('/version')
def getJavaVersion():
    print("version")
    a = subprocess.run(['java', '--version'], capture_output=True, shell=True)
    print(a.stdout)
    return str(a.stdout), 200


@bp.route('/startparamter', methods=["POST"])
def startNuvoLedWithParameter():
    global proc, child_pid, running
    if running:
        return "failed to launch | another instance is running", 404
    running = True
    request_data = request.get_json()
    print(str(request_data))
    proc = subprocess.Popen(["java", "-jar", "nuvoled-1.0-SNAPSHOT-jar-with-dependencies.jar", "-py",
                             str(request_data["py"]), "-px",
                             str(request_data["px"]), "-br", str(request_data["brightness"]), "-r",
                             str(request_data["rotation"]), "-sn", str(request_data["screennumber"])],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    child_pid = proc.pid
    createStatusLoop()
    return "started", 200


@bp.post('/start')
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


@bp.get('/status')
def getAllStatus():
    status = "Status:"
    if (q.empty()):
        return "nothing in que", 200
    while not q.empty():
        status = status + str(q.get(timeout=1))
    return status, 200


@bp.get('/ip')
def getip():
    if sys.platform == "win32":
        output = subprocess.run("ipconfig", capture_output=True, shell=True)
        return str(output.stdout), 200
    else:
        output = subprocess.Popen(["ifconfig"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        line = output.stdout.read().decode()
        return line, 200


@bp.get('/ipstate')
def getipstate():
    # find ip 169.254
    if sys.platform == "win32":
        output = subprocess.run("ipconfig", capture_output=True, shell=True)
        return findNuvoIp(str(output.stdout)), 200
    else:
        output = subprocess.Popen(["ifconfig"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        line = output.stdout.read().decode()
        return findNuvoIp(line), 200


@bp.post('/startchromium')
def startChromium():
    global chromeId, runningChrome
    chrome = subprocess.Popen(["chromium", "--kiosk", "http://localhost/display/"], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    chromeId = chrome.pid
    runningChrome = True
    return "started", 200


@bp.post('/stopchromium')
def stopChromium():
    global runningChrome
    kills(chromeId)
    runningChrome = False
    return "stopped", 200

@bp.get('/statuschrome')
def getStatusChrome():
    global runningChrome
    if runningChrome:
        stateJava = { "state": True }
        return stateJava, 200
    else:
        stateJava = { "state": False }
        return stateJava, 200

@bp.get('/statusonoff')
def getStatus():
    if running:
        stateJava = { "state": True }
        return stateJava, 200
    else:
        stateJava = { "state": False }
        return stateJava, 200


@bp.post('/stop')
def stopNuvoLed():
    global proc, running
    running = False
    print("terminate")
    kills(child_pid)
    (output, error) = proc.communicate()
    s = error + output
    proc = None

    return str(s), 200
