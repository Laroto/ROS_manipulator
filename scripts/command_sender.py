#!/usr/bin/env python
import serial
import time
import rospy
from neeeilit.msg import arm_pos

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)

def callback (data):
    cmd = str(data.joint1) + ';' + str(data.joint2) + ';' + str(data.joint3) + ';' + str(data.joint4) + ';' + str(data.gripper)
    arduino.write(bytes(cmd, 'utf-8'))
    time.sleep(0.05)

def listener():
    rospy.init_node('command_sender', anonymous=True)
    rospy.Subscriber ('/cmd',arm_pos,callback)    
    #timer = rospy.Timer(rospy.Duration(0.1), timer_callback)
    #print ("Last message published")
    rospy.spin()    
    
if __name__ == '__main__':
    listener()