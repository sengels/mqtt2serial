#!/usr/bin/python3
from daemon.runner import DaemonRunner
import time
import logging
from mqtt2serial import main

class MqttDaemonRunner(DaemonRunner):
    def _open_streams_from_app_stream_paths(self, app):
        """ Open the `daemon_context` streams from the paths specified.
    
            :param app: The application instance.
    
            Open the `daemon_context` standard streams (`stdin`,
            `stdout`, `stderr`) as stream objects of the appropriate
            types, from each of the corresponding filesystem paths
            from the `app`.
            """
        self.daemon_context.stdin = open(app.stdin_path, 'rt')
        self.daemon_context.stdout = open(app.stdout_path, 'w+t')
        self.daemon_context.stderr = open(app.stderr_path, 'w+t')

class MqttApp(object):
    def __init__(self):
        self.stdout_path = '/dev/null'
        self.stderr_path = '/dev/null'
        self.stdin_path = '/dev/null'
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

run = MqttDaemonRunner(MqttApp())
run.do_action()
