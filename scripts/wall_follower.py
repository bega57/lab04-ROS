#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from utils import clean


class WallFollower:
    def __init__(self):
        rospy.init_node('wall_follower')
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        rospy.Subscriber('/scan', LaserScan, self.scan_callback)

        self.desired_wall_dist = 0.5   # Soll-Abstand zur Wand
        self.front_threshold = 0.6     # ab wann Wand vorne erkannt
        self.state = 'FIND_WALL'       # FIND_WALL, TURN, FOLLOW_WALL

        rospy.loginfo('Wall Follower started')
        rospy.spin()

    def scan_callback(self, data):
        front_vals = clean(data.ranges[0:10] + data.ranges[350:360])
        right_vals = clean(data.ranges[260:280])
        front = min(front_vals) if front_vals else 10.0
        right = min(right_vals) if right_vals else 10.0

        twist = Twist()

        if self.state == 'FIND_WALL':
            if front < self.front_threshold:
                self.state = 'TURN'
                rospy.loginfo('Wall found! Turning...')
            else:
                twist.linear.x = 0.2

        elif self.state == 'TURN':
            if front > self.front_threshold and right < 1.0:
                self.state = 'FOLLOW_WALL'
                rospy.loginfo('Following wall...')
            else:
                twist.angular.z = 0.5

        elif self.state == 'FOLLOW_WALL':
            if front < self.front_threshold:
                self.state = 'TURN'
                rospy.loginfo('Wall ahead, turning...')
            else:
                twist.linear.x = 0.15
                error = self.desired_wall_dist - right
                twist.angular.z = -error * 2.0
                if right > 1.5:
                    twist.angular.z = -0.3

        if not rospy.is_shutdown():
            self.pub.publish(twist)


if __name__ == '__main__':
    try:
        WallFollower()
    except rospy.ROSInterruptException:
        pass
