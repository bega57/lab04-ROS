#!/usr/bin/env python3
import rospy
import csv
import os
from datetime import datetime
from lab4.msg import RobotStatus
from lab4.srv import ToggleLogging, ToggleLoggingResponse

class Logger:
    def __init__(self):
        rospy.init_node('logger')
        self.logging_enabled = True
        self.log_dir = os.path.expanduser('~/catkin_ws/src/lab4/logs')
        os.makedirs(self.log_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file = os.path.join(self.log_dir, f'log_{timestamp}.csv')

        with open(self.log_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'lin_x', 'ang_z',
                             'front', 'left', 'right'])

        rospy.Service('/toggle_logging', ToggleLogging, self.handle_toggle)
        rospy.Subscriber('/robot_status', RobotStatus, self.status_callback)

        rospy.loginfo(f'Logger started. File: {self.log_file}')
        rospy.loginfo('Logging is ON. Call /toggle_logging to switch.')
        rospy.spin()

    def handle_toggle(self, req):
        self.logging_enabled = req.enable
        state = 'enabled' if req.enable else 'disabled'
        rospy.loginfo(f'Logging {state}')
        return ToggleLoggingResponse(success=True, message=f'Logging {state}')

    def status_callback(self, data):
        if not self.logging_enabled:
            return
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                rospy.get_time(),
                data.velocity.linear.x,
                data.velocity.angular.z,
                data.front_distance,
                data.left_distance,
                data.right_distance
            ])

if __name__ == '__main__':
    try:
        Logger()
    except rospy.ROSInterruptException:
        pass
