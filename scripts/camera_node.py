#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class CameraNode:
    def __init__(self):
        rospy.init_node('camera_node')
        self.bridge = CvBridge()
        rospy.Subscriber('/camera/rgb/image_raw', Image, self.image_callback)
        rospy.loginfo('Camera node started')
        rospy.spin()

    def image_callback(self, data):
        cv_image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        cv2.imshow('Camera - Original', cv_image)
        cv2.imshow('Camera - Edges', edges)
        cv2.waitKey(1)


if __name__ == '__main__':
    try:
        CameraNode()
    except rospy.ROSInterruptException:
        pass
