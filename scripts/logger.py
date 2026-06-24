#!/usr/bin/env python3
import rospy
import csv
import os
from datetime import datetime
from lab4.msg import RobotStatus


class Logger:
    def __init__(self):
        rospy.init_node('logger')
        self.log_dir = os.path.expanduser('~/catkin_ws/src/lab4/logs')
        os.makedirs(self.log_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file = os.path.join(self.log_dir, f'log_{timestamp}.csv')

        with open(self.log_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'lin_x', 'ang_z',
                             'front', 'left', 'right'])

        rospy.Subscriber('/robot_status', RobotStatus, self.status_callback)

        rospy.loginfo(f'Logger started. File: {self.log_file}')
        rospy.spin()

    def status_callback(self, data):
        if not rospy.get_param('/logging_enabled', True):
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
