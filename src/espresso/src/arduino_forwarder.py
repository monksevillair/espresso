#!/usr/bin/env python
from std_msgs.msg import Int32
import geometry_msgs.msg
import serial
import rospy
import math
import time
import tf

ser = serial.Serial('/dev/ttyArduinoAuger', 115200)  # open serial port
print(ser.name)         # check which port was really used

rospy.init_node('arduino_passthrough_valve')

def target_callback(msg):
    v = 'a'+str(int(msg.data))+'\n'
    print v
    ser.write(v)     # write a string

def tip_auger_callback(msg):
    v = 'b'+str(int(msg.data))+'\n'
    print v
    ser.write(v)     # write a string


target_sub = rospy.Subscriber('/valve_target', Int32, target_callback)
target_sub = rospy.Subscriber('/tip_auger', Int32, tip_auger_callback)

time.sleep(2)
print "Arduino Passthrough ready"

rate = rospy.Rate(140.0)
while not rospy.is_shutdown():
    rate.sleep()

ser.close()             # close port
