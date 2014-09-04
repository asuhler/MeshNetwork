#!/usr/bin/env python
'''battery commands'''

from pymavlink import mavutil
from MAVProxy.modules.lib import mp_module




class HelloModule(mp_module.MPModule):
    def __init__(self, mpstate):
        super(HelloModule, self).__init__(mpstate, "loiter", "battery commands")
        self.add_command('loiter', self.hello, "show battery information")
        self.lat = 380636367
        self.lon = -774964877
        self.alt = 100

    def hello(self, args):
        print "sending a loiter yay!!!!"
        self.master.mav.command_long_send (self.target_system, self.target_component,
                                       mavutil.mavlink.MAV_CMD_NAV_LOITER_UNLIM, 0, 0, 0, 0, 0, self.lat, self.lon, self.alt)
        '''self.master.mav.mission_item_send (self.status.target_system,
                                           self.status.target_component,
                                           1,
                                           0,
                                           mavutil.mavlink.MAV_CMD_NAV_LOITER_UNLIM,
                                           2, 1, 3, 4, 1, 5, self.lat, self.lon, self.alt)'''

    def mavlink_packet(self, m):
        '''handle a mavlink packet'''
        mtype = m.get_type()
        #if mtype == "SYS_STATUS":
            #print "I got a status packet"

def init(mpstate):
    '''initialise module'''
    return HelloModule(mpstate)
