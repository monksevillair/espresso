#!/usr/bin/env python
from std_msgs.msg import Float32, Int32
import geometry_msgs.msg
import rospy
import math
import time
import tf

class StateMachine:
    def __init__(self):
        rospy.init_node('arduino_passthrough_valve')
        self.weight = -100.0
        self.hall = 0

        target_sub = rospy.Subscriber('/weight', Float32, self.weight_callback)
        target_sub = rospy.Subscriber('/hall', Int32, self.hall_callback)
        self.table_pub = rospy.Publisher('/hall', Int32, queue_size=10)
        time.sleep(0.5)
        
        print "state machine started"
        
        rate = rospy.Rate(150.0)
        
        while not rospy.is_shutdown():

            # TODO: State machine
            #   - assume in fully extended position
            #   - rotate clockwise for 4.5s at 0.7 duty 14.5v to stop
            #   - dispense cup
            #   - rotate to hall sensor -0.7 duty
            #   - dispense drink
            #   - rotate to end point for 3.5s at -0.7 duty
            # exit program
            
            rate.sleep()

        print "exiting"

    def weight_callback(self, msg):
        self.weight = msg.data

    def hall_callback(self, msg):
        self.hall = msg.data

if __name__ == '__main__':
    state_machine = StateMachine()
