#!/usr/bin/python3
from daemon import DaemonContext
from lockfile import FileLock
import time
import logging
from mqtt2serial import main

class MqttApp(object):
    def __init__(self):
        self.pidfile_path = '/var/run/mqtt2seriald.pid'
        self.pidfile_timeout = 10

    def run(self):
        logging.basicConfig(format="%(asctime)s [ARDUINO/%(processName)s] %(levelname)s %(message)s",
                            filename='/var/log/nagf2rpi/mqtt2seriald.log',
                            level=logging.DEBUG)
        logging.info("Starting")
        try:
            logging.info("before main")
            main(logging)
        except(SystemExit, KeyboardInterrupt):
            logging.info("Exiting normally...")
        except:
            logging.exception("some exception")

app = MqttApp()
with DaemonContext(pidfile=FileLock(app.pidfile_path, app.pidfile_timeout)):
    app.run()
