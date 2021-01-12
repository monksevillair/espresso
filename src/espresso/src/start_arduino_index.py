#!/usr/bin/env python
import serial
import rospy
from std_msgs.msg import Int32

arduino = serial.Serial('/dev/ttyArduinoIndex', 115200, timeout=.1)

pub = rospy.Publisher('/hall', Int32, queue_size=10)
rospy.init_node('talker', anonymous=True)

pub_once = True

while not rospy.is_shutdown():
    data = arduino.readline()[:-2] #the last bit gets rid of the new-line chars

    #print data
    if data:
        try:
            print data
            ar = Int32(data=int(data))
            pub.publish(ar)
        except:
            pass

