#!/usr/bin/env python
import serial
import rospy
from std_msgs.msg import Float32MultiArray

arduino = serial.Serial('/dev/ttyArduinoB', 115200, timeout=.1)
##while True:
##    data = arduino.readline()[:-2] #the last bit gets rid of the new-line chars
##    if data:
##	print data[:-2].split(" ")


pub = rospy.Publisher('/pot_box', Float32MultiArray, queue_size=10)
rospy.init_node('talker', anonymous=True)

margin = 0.01
pub_once = True
l_dat = []

while not rospy.is_shutdown():
    data = arduino.readline()[:-2] #the last bit gets rid of the new-line chars

    print data
    
    if data:
        try:
            dat = [float(x)/512.0-1.0 for x in data[:-1].split(" ")]
            ar = Float32MultiArray(data=dat)
            pub.publish(ar)
        except:
            pass

