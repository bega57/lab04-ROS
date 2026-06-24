#!/usr/bin/env python3
import rospy
from lab4.srv import ToggleLogging, ToggleLoggingResponse


class LoggingControl:
    def __init__(self):
        rospy.init_node('logging_control')
        rospy.set_param('/logging_enabled', True)
        rospy.Service('/toggle_logging', ToggleLogging, self.handle_toggle)
        rospy.loginfo('Logging control ready. Logging is ON. Call /toggle_logging to switch.')
        rospy.spin()

    def handle_toggle(self, req):
        rospy.set_param('/logging_enabled', req.enable)
        state = 'enabled' if req.enable else 'disabled'
        rospy.loginfo(f'Logging {state}')
        return ToggleLoggingResponse(success=True, message=f'Logging {state}')


if __name__ == '__main__':
    try:
        LoggingControl()
    except rospy.ROSInterruptException:
        pass
