#!/usr/bin/env python3
import math
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from lab4.msg import RobotStatus


def clean(values):
    return [r for r in values if r > 0.0 and not math.isinf(r) and not math.isnan(r)]


class StatusPublisher:
    def __init__(self):
        rospy.init_node('status_publisher')
        self.pub = rospy.Publisher('/robot_status', RobotStatus, queue_size=10)
        self.current_vel = Twist()
        self.front = 0.0
        self.left = 0.0
        self.right = 0.0

        rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        rospy.Subscriber('/cmd_vel', Twist, self.vel_callback)

        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            msg = RobotStatus()
            msg.velocity = self.current_vel
            msg.front_distance = self.front
            msg.left_distance = self.left
            msg.right_distance = self.right
            self.pub.publish(msg)
            rate.sleep()

    def scan_callback(self, data):
        front_vals = clean(data.ranges[0:10] + data.ranges[350:360])
        left_vals = clean(data.ranges[80:100])
        right_vals = clean(data.ranges[260:280])
        self.front = min(front_vals) if front_vals else 10.0
        self.left = min(left_vals) if left_vals else 10.0
        self.right = min(right_vals) if right_vals else 10.0

    def vel_callback(self, data):
        self.current_vel = data


if __name__ == '__main__':
    try:
        StatusPublisher()
    except rospy.ROSInterruptException:
        pass
