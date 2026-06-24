#!/usr/bin/env python3
import csv
import os
from datetime import datetime

import rospy
import rospkg

from lab4.msg import RobotStatus


class Logger:
    def __init__(self):
        rospy.init_node('logger')

        package_path = rospkg.RosPack().get_path('lab4')
        default_log_dir = os.path.join(package_path, 'logs')
        self.log_dir = rospy.get_param('~log_dir', default_log_dir)
        os.makedirs(self.log_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file = os.path.join(self.log_dir, f'robot_status_{timestamp}.csv')

        with open(self.log_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'ros_time',
                'wall_time',
                'linear_x',
                'angular_z',
                'front_distance',
                'left_distance',
                'right_distance'
            ])

        rospy.Subscriber('/robot_status', RobotStatus, self.status_callback)
        rospy.loginfo(f'Logger started. Writing to: {self.log_file}')
        rospy.spin()

    def status_callback(self, data):
        if not rospy.get_param('/logging_enabled', True):
            return

        ros_time = rospy.Time.now().to_sec()
        wall_time = datetime.now().isoformat(timespec='seconds')

        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                ros_time,
                wall_time,
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
