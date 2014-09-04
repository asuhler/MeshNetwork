#!/usr/bin/env python
'''battery commands'''


from MAVProxy.modules.lib import mp_module


class BatteryModule(mp_module.MPModule):
    def __init__(self, mpstate):
        super(BatteryModule, self).__init__(mpstate, "battery", "battery commands")
        self.add_command('bat', self.hello, "show battery information")

    def hello(self):
        print "Hello"


    def mavlink_packet(self, m):
        '''handle a mavlink packet'''
        mtype = m.get_type()
        if mtype == "SYS_STATUS":
            print "I got a status packet"

def init(mpstate):
    '''initialise module'''
    return BatteryModule(mpstate)
