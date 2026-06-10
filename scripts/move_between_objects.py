#!/usr/bin/env python3
import math
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


def clean(values):
    return [r for r in values if r > 0.0 and not math.isinf(r) and not math.isnan(r)]


class MoveBetweenObjects:
    def __init__(self):
        rospy.init_node('move_between_objects')
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        rospy.Subscriber('/scan', LaserScan, self.scan_callback)

        self.min_distance = 0.5
        self.direction = 'FORWARD'
        self.last_switch = rospy.Time.now()
        self.cooldown = rospy.Duration(2.0)  # 2s Sperre nach Richtungswechsel

        rospy.loginfo('Move Between Objects started')
        rospy.spin()

    def scan_callback(self, data):
        front_vals = clean(data.ranges[0:10] + data.ranges[350:360])
        back_vals = clean(data.ranges[170:190])
        front = min(front_vals) if front_vals else 10.0
        back = min(back_vals) if back_vals else 10.0

        twist = Twist()
        now = rospy.Time.now()
        can_switch = (now - self.last_switch) > self.cooldown

        if self.direction == 'FORWARD':
            if front < self.min_distance and can_switch:
                self.direction = 'BACKWARD'
                self.last_switch = now
                rospy.loginfo('Object ahead! Reversing...')
            else:
                twist.linear.x = 0.2
        elif self.direction == 'BACKWARD':
            if back < self.min_distance and can_switch:
                self.direction = 'FORWARD'
                self.last_switch = now
                rospy.loginfo('Object behind! Going forward...')
            else:
                twist.linear.x = -0.2

        self.pub.publish(twist)


if __name__ == '__main__':
    try:
        MoveBetweenObjects()
    except rospy.ROSInterruptException:
        pass
