#!/usr/bin/env python

import math
import time
import rospy
from std_msgs.msg import Float64, String

extender_current = 0.0;

def extender_current_callback(msg):
    global extender_current

    extender_current = msg.data
    
def talker():
    global mode, extender_current
    
    rospy.init_node('test_extender', anonymous=True)
    rate = rospy.Rate(100) # 10hz

    extender_pub = rospy.Publisher('/vesc_extender/command/duty_cycle', Float64, queue_size=1)

    rospy.Subscriber("/vesc_extender/state/current_motor", Float64, extender_current_callback)

    last_time = time.time()
    
    while not rospy.is_shutdown():
        extender_sp_msg = Float64()


        extender_sp_msg.data = -0.55
        extender_pub.publish(extender_sp_msg)

        rate.sleep()
        
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
