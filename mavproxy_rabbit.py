#!/usr/bin/env python
'''battery commands'''

import time, math
import threading
import pika
import sys
from pymavlink import mavutil
from MAVProxy.modules.lib import mp_module
from MAVProxy.modules.lib.mp_settings import MPSetting

class vars(object):
    commands = str()
    rabbit = object
    username = 'UAS'
    password = 'UAS'
    host = '10.128.4.222'
    vhost = 'UASHost'
    exchange = 'UAS'

    def startRabbit(self):
        try:
            creds = pika.PlainCredentials(username=self.username, password=self.password)
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(\
                host = self.host,\
                virtual_host = self.vhost,\
                credentials = creds))
            self.channel = self.connection.channel()

            self.channel.exchange_declare(exchange = self.exchange, \
                                     type = 'topic')


            self.connectionPublish = pika.BlockingConnection(pika.ConnectionParameters(\
                host = self.host,\
                virtual_host = self.vhost,\
                credentials = creds))

            self.publishChannel = self.connectionPublish.channel()

            self.publishChannel.exchange_declare(exchange = self.exchange, \
                                 type = 'topic')


            result = self.channel.queue_declare(exclusive = True)
            queue_name = result.method.queue

            binding_keys = ['Ardupilot.data.commands.1']

            self.channel.queue_bind(exchange = self.exchange, \
                       queue = queue_name, \
                       routing_key = "Autopilot.commands")

            self.channel.basic_consume(callback, \
                          queue = queue_name, \
                          no_ack = True)

            print "Connected to rabbit server"
        except:
            print "Failed to connect to the rabbit server"


class Threaded(object):
    def __init__(self, function, *args, **kwargs):
        print "The threaded object initalized"
        self.thread = None
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        #self.setDaemon = True


    def start(self):
        self.thread = threading.Thread(target = self.function)
        self.thread.start()


    def stop(self):
            print "it stopped"
            #Vars.connection.close()
            self.thread.join(None)
            #Vars.enough = True
            sys.exit(0)
            #self.thread.join()



def callback(ch, method, properties, body):
        print "[x] %s: %s: %s" % (str(time.time()), method.routing_key, str(body))
        input = body.split(",")
        if len(input)>0:
            if input[0] == "Loiter":
                if len(input) == 4:
                    args = [str(input[1]), str(input[3]), str(input[3])]
                    sendGuidedPoint(args)
                    #print args
                else:
                    print "No actionable commands in Loiter packet"
            elif input[0] == "Land":
                sendLand("hi")
        else:
            print "Empty message received from rabbit"


def startConsuming():
    try:
        print "Started consuming"
        Vars.channel.start_consuming()
    except:
        print "Failed to start consuming"

def sendGuidedPoint(args):
    print "sending a guided point yay!!!!"
    Vars.rabbit.sendGuided(args)

def sendLand(args):
    Vars.rabbit.land(args)


class Rabbit(mp_module.MPModule):

    def __init__(self, mpstate):
        super(Rabbit, self).__init__(mpstate, "rabbit", "Rabbit commands", True)
        self.add_command('Loiter', self.sendGuided, "send guided command")
        self.add_command('Land', self.land, "Lands the copter at its current location")
        #print "command added"
        Vars.startRabbit()
        consume.start()

    def land(self, args):
        self.master.mav.set_mode_send(self.master.target_system, mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, 9)

    def sendGuided(self, args):
        #print args
        if len(args) == 3:
            lat = float(args[0])
            lon = float(args[1])
            alt = float(args[2])
            print "sending a guided point yay!!!!"
            self.master.mav.mission_item_send (self.status.target_system,
                                               self.status.target_component,
                                               0,
                                               0,
                                               mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                                               2, 0, 1, 0, 0, 0,
                                               lat, lon, alt)
            self.master.mav.set_mode_send(self.master.target_system, mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, 4) #4 for copters, #8 for planes
        else:
            print "Failed to enter arguments correctly: Usage: Loiter lat lon alt"
            return

    def mavlink_packet(self, m):
        '''handle a mavlink packet'''
        mtype = m.get_type()
        #print m
        if mtype == 'waypoint 15':
            #print m
            hi = m
            #placeholder: only sent from the autopilot when the waypoint is changed
        if mtype == 'MISSION_CURRENT':
            #print m
            hi = m
            #placeholder: Continuously pushed the waypoint it's going to
        if mtype == 'GPS_RAW_INT':
            #print m
            input = str(m).split(',')
            i=0
            while i<len(input):
                input[i] = input[i].strip()
                i=i+1
            if len(input)>0:
                gpsdata = [input[2], input[3]]
                i=0
                while i<len(gpsdata):
                    splitstring = gpsdata[i].split(" : ")
                    gpsdata[i] = splitstring[1]
                    i=i+1

                #print "Lat: " + str(gpsdata[0]) + "   Lon: " + str(gpsdata[1])
                publishSomething("Lat: " + str(gpsdata[0]) + "   Lon: " + str(gpsdata[1]))

            else:
                print "NoGPS data in packet, something went realllyyy wrong"
        #elif mtype == "SYS_STATUS":
            #print m




def publishSomething(body):
    try:
        Vars.publishChannel.basic_publish(exchange=Vars.exchange, \
        routing_key='hello.out',\
        body=body)
    except:
        print "Failed to publish to the rabbit server"

Vars = vars()
consume = Threaded(startConsuming)


def init(mpstate):
    Vars.rabbit = Rabbit(mpstate)
    '''initialise module'''
    return Vars.rabbit