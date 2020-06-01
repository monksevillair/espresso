#!/usr/bin/env python

import math
import time
import rospy
from std_msgs.msg import Float64, String

#MODES:
# MOVE_TO_GRINDER, MOVE_TO_GROUPHEAD, ATTACH_TO_GROUPHEAD, ROTATE_PORTAFILTER_IN, ROTATE_PORTAFILTER_OUT, DETACH_FROM_GROUPHEAD
mode = "MOVE_TO_GRINDER"
#mode = "DETACH_FROM_GROUPHEAD"
rotate_current = 0.0;

def rotate_current_callback(msg):
    global rotate_current

    rotate_current = msg.data
    
def talker():
    global mode, rotate_current
    
    rospy.init_node('test_arm', anonymous=True)
    rate = rospy.Rate(100) # 10hz

    portafilter_pub = rospy.Publisher('/vesc_portafilter/command/duty_cycle', Float64, queue_size=1)
    tilt_pub = rospy.Publisher('/vesc_tilt/command/current', Float64, queue_size=1)
    rotate_pub = rospy.Publisher('/vesc_rotate/command/duty_cycle', Float64, queue_size=1)

    rospy.Subscriber("/vesc_rotate/state/current_motor", Float64, rotate_current_callback)

    last_time = time.time()
    
    while not rospy.is_shutdown():
        portafilter_sp_msg = Float64()
        #portafilter_sp_msg.data = -0.8

        tilt_sp_msg = Float64()
        #tilt_sp_msg.data = -1.0

        rotate_sp_msg = Float64()

        if mode == "MOVE_TO_GRINDER":
            rotate_sp_msg.data = -0.15
            rotate_pub.publish(rotate_sp_msg)
            if abs(rotate_current) > 1.1:
                mode = "MOVE_TO_GROUPHEAD"
                last_time = time.time()
            
        if mode == "MOVE_TO_GROUPHEAD":
            if time.time()-last_time > 2:
                rotate_sp_msg.data = 0.15
                rotate_pub.publish(rotate_sp_msg)
                if abs(rotate_current) > 0.6:
                    mode = "ATTACH_TO_GROUPHEAD"
                    last_time = time.time()

        if mode == "ATTACH_TO_GROUPHEAD":
            tilt_sp_msg.data = 1.0
            tilt_pub.publish(tilt_sp_msg)
            if time.time()-last_time > 2:
                portafilter_sp_msg.data = 0.8
                portafilter_pub.publish(portafilter_sp_msg)
            if time.time()-last_time > 11:
                mode = "DETACH_FROM_GROUPHEAD"
                last_time = time.time()

        if mode == "DETACH_FROM_GROUPHEAD":
            if time.time()-last_time > 5:
                portafilter_sp_msg.data = -0.8
                portafilter_pub.publish(portafilter_sp_msg)
            if time.time()-last_time > 6+9:
                tilt_sp_msg.data = -1.0
                tilt_pub.publish(tilt_sp_msg)
                mode = "MOVE_TO_GRINDER"
                last_time = time.time()

        print mode

        #portafilter_pub.publish(portafilter_sp_msg)
        #tilt_pub.publish(tilt_sp_msg)
        

        rate.sleep()
        
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
