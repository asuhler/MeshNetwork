#!/usr/bin/env python
'''battery commands'''

import time, math
import threading
import pika
import sys
from MAVProxy.modules.lib import mp_module


class Rabbit(mp_module.MPModule):
    def __init__(self, mpstate):
        super(Rabbit, self).__init__(mpstate, "rabbit", "rabbit stuff")
        self.add_command('rabbit', self.hello, "rabbit information")

    def hello(self):
        print "Hello"


    def mavlink_packet(self, m):
        '''handle a mavlink packet'''
        mtype = m.get_type()
        if mtype == "SYS_STATUS":
            print "I am rabbit, and I got a status packet"

    class vars():
        hello = str()

def init(mpstate):
    Vars = vars()
    '''initialise module'''
    return Rabbit(mpstate)
