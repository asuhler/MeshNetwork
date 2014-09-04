#!/usr/bin/env python

from pymavlink import mavutil
from MAVProxy.modules.lib import mp_module
#define AUTO 3
class Loiter(mp_module.MPModule):
    def __init__(self, mpstate):
        super(Loiter, self).__init__(mpstate, "loitertest", "battery commands")
        self.add_command('loiter', self.hello, "show battery information")
        self.lat = float(37.0640602111816)
        self.lon = float(-76.4972381591797)
        self.alt = 100

    def hello(self, args):
        print "sending a guided point yay!!!!"
        if len(args)==0:
            self.lat = float(37.0640602111816)
            self.lon = float(-76.4972381591797)
            self.alt = 1
        else:
            self.lat = float(args[0])
            self.lon = float(args[1])
            self.alt = int(args[2])
        self.master.mav.mission_item_send (self.status.target_system,
                                           self.status.target_component,
                                           0,
                                           0,
                                           mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                                           2, 0, 1, 0, 0, 0,
                                           self.lat, self.lon, self.alt)
        self.master.mav.set_mode_send(self.master.target_system, mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, 4)

    def mavlink_packet(self, m):
        #just left this open for functionality if I needed it for testing later
        mtype = m.get_type()


def init(mpstate):
    return Loiter(mpstate)


#define STABILIZE 0                     // hold level position
#define ACRO 1                          // rate control
#define ALT_HOLD 2                      // AUTO control
#define AUTO 3                          // AUTO control
#define GUIDED 4                        // AUTO control
#define LOITER 5                        // Hold a single location
#define RTL 6                           // AUTO control
#define CIRCLE 7                        // AUTO control
#define POSITION 8                      // AUTO control
#define LAND 9                          // AUTO control
#define OF_LOITER 10                    // Hold a single location using optical flow
                                        # sensor
#define TOY_A 11                        // THOR Enum for Toy mode
#define TOY_M 12                        // THOR Enum for Toy mode
#define NUM_MODES 13