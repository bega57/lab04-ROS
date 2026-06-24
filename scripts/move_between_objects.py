#!/usr/bin/env python3
import math

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


def clean(values):
    return [r for r in values if r > 0.0 and not math.isinf(r) and not math.isnan(r)]


class MoveBetweenObjects:
    def __init__(self):
        rospy.init_node('move_between_objects')

        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        rospy.Subscriber('/scan', LaserScan, self.scan_callback)

        self.stop_distance = rospy.get_param('~stop_distance', 0.65)
        self.object_detection_range = rospy.get_param('~object_detection_range', 3.5)
        self.speed = rospy.get_param('~speed', 0.18)

        self.direction = 'FORWARD'
        self.last_switch = rospy.Time.now()
        self.cooldown = rospy.Duration(1.5)

        rospy.loginfo('Move Between Objects started')
        rospy.spin()

    def get_min_distance(self, ranges, start, end):
        values = clean(ranges[start:end])
        return min(values) if values else 10.0

    def scan_callback(self, data):
        front_values = data.ranges[0:15] + data.ranges[345:360]
        back_values = data.ranges[165:195]

        front = min(clean(front_values)) if clean(front_values) else 10.0
        back = min(clean(back_values)) if clean(back_values) else 10.0

        front_object_detected = front < self.object_detection_range
        back_object_detected = back < self.object_detection_range

        twist = Twist()
        now = rospy.Time.now()
        can_switch = (now - self.last_switch) > self.cooldown

        rospy.loginfo_throttle(
            2.0,
            f'front={front:.2f}m detected={front_object_detected}, '
            f'back={back:.2f}m detected={back_object_detected}, direction={self.direction}'
        )

        if not front_object_detected and not back_object_detected:
            twist.linear.x = 0.0
            if not rospy.is_shutdown():
                if not rospy.is_shutdown():
            self.pub.publish(twist)
            return

        if self.direction == 'FORWARD':
            if front_object_detected and front <= self.stop_distance and can_switch:
                self.direction = 'BACKWARD'
                self.last_switch = now
                rospy.loginfo('Front object reached. Switching to BACKWARD.')
            else:
                twist.linear.x = self.speed

        elif self.direction == 'BACKWARD':
            if back_object_detected and back <= self.stop_distance and can_switch:
                self.direction = 'FORWARD'
                self.last_switch = now
                rospy.loginfo('Back object reached. Switching to FORWARD.')
            else:
                twist.linear.x = -self.speed

        if not rospy.is_shutdown():
            self.pub.publish(twist)


if __name__ == '__main__':
    try:
        MoveBetweenObjects()
    except rospy.ROSInterruptException:
        pass
