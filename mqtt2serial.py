import paho.mqtt.client as mqtt
import serial
import sys
try:
    from Queue import Queue
except:
    from queue import Queue
logging = None

q=Queue()

receive_topic = '/home/nagf2rpi/basestation_serial'
send_topic = '/home/nagf2rpi/basestation_serial_answer'
serial_device = '/dev/ttyUSB0'
#serial_device = '/dev/ttyACM0'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logging.debug("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(receive_topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    logging.debug(msg.topic + " " + str(msg.payload) + "!")
    q.put(msg.payload)

def main(log):
    global logging
    logging = log
    s = None
    logging.debug("main!")
    try:
        s = serial.Serial(serial_device, 115200, timeout=0)
    except serial.serialutil.SerialException as e:
        logging.debug("failed to open serial console \n({0} - {1})".format(e.errno, e.strerror))
    except:
        logging.debug("Unexpected:", sys.exc_debug()[0])
        raise
    logging.debug('managed to open serial console')

    client = mqtt.Client()
    logging.debug('trying to start mqttclient')

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost", 1883, 60)

    while True:
        client.loop(.1)
        while not q.empty():
            data = q.get()
            logging.debug('writing:{}{}'.format(data, type(data)))
            if data is None:
                continue
            try:
                s.write(data)
            except serial.serialutil.SerialException as e:
                logging.debug("failed to write serial console \n({0} - {1})".format(e.errno, e.strerror))
            except:
                logging.debug("Unexpected:", sys.exc_info()[0])
                raise
        try:
            if s and s.inWaiting() > 0:
                data = s.read(s.inWaiting())
                if len(data) > 0:
                    client.publish(send_topic, data)
                    logging.debug('reading: {}'.format(data))
        except OSError as e:
            data = s.read(1)
            logging.debug("OSERROR!")
            if len(data) > 0:
                client.publish(send_topic, data)
                logging.debug('reading: {}'.format(data))
        except serial.serialutil.SerialException as e:
            logging.debug("failed to read serial console \n({0} - {1})".format(e.errno, e.strerror))
        except:
            logging.debug("Unexpected:", sys.exc_info())
            raise

if __name__ == '__main__':
    import logging
    logging.basicConfig(filename='/var/log/nagf2rpi/mqtt2serial.log', level=logging.DEBUG)
    logging.debug("test mqtt2serial")
    main(logging)
