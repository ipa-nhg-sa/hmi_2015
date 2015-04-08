#!/usr/bin/python
import roslib
roslib.load_manifest('hmi_scenario_states')
import rospy
import smach
import smach_ros
import sys

import random


from simple_script_server import *
sss = simple_script_server()

## This script does not move the Robot.
## COB4 only changes colors and mimics.
## One can use this script while charging for entertainment.

## -- Initiation
class CobColorsInit(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
            outcomes=['succeeded','failed'])
            
    def execute(self, userdata):
        #handle_base = sss.init("base")
        #handle_arm_left = sss.init("arm_left")
        #handle_arm_right = sss.init("arm_right")
        #handle_sensorring = sss.init("sensorring")

        #if handle_base.get_error_code() != 0:
        #    return "failed"
        #if handle_arm_left.get_error_code() != 0:
        #    return "failed"
        #if handle_arm_right.get_error_code() != 0:
        #    return "failed"
        #if handle_sensorring.get_error_code() != 0:
            #return "failed"

        return "succeeded"
## -- Recover
class CobColorsRecover(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
            outcomes=['succeeded','failed'])
            
    def execute(self, userdata):
        #handle_base = sss.recover("base")
        #handle_arm_left = sss.recover("arm_left")
        #handle_arm_right = sss.recover("arm_right")
        #handle_sensorring = sss.recover("sensorring")

        #if handle_base.get_error_code() != 0:
        #    return "failed"
        #if handle_arm_left.get_error_code() != 0:
        #    return "failed"
        #if handle_arm_right.get_error_code() != 0:
        #    return "failed"
        #if handle_sensorring.get_error_code() != 0:
            #return "failed"

        return "succeeded"

## -- Prepare
class CobColorsPrepare(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
            outcomes=['succeeded','failed'])
            
    def execute(self, userdata):
        #handle_arm_left = sss.move("arm_left", "folded",False)
        #handle_arm_right = sss.move("arm_right", "folded",False)
        #handle_sensorring = sss.move("sensorring", "front",False)

        #handle_arm_left.wait()
        #handle_arm_right.wait()
        #handle_sensorring.wait()

        #if handle_arm_left.get_error_code() != 0:
        #    return "failed"
        #if handle_arm_right.get_error_code() != 0:
        #    return "failed"
        #if handle_sensorring.get_error_code() != 0:
            #return "failed"

        return "succeeded"

## -- main script
class CobColors(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
            outcomes=['succeeded','failed'])
            
    def execute(self, userdata):
        
        sleep_time = 20
        
        rospy.loginfo("This script does not move the Robot.")
        rospy.loginfo("COB4 only changes colors and mimics.")
        rospy.loginfo("You can use this script while charging for entertainment.")
        rospy.loginfo("Sleep time is set to: " + str(sleep_time) +" sec")
        
        sss.set_light("light_base","cyan",False)
        sss.set_light("light_torso", "cyan")
        
        while True:
            rospy.sleep(sleep_time)
            sss.set_mimic("mimic","bored")
            sss.set_light("light_base","blue")
            rospy.sleep(2)
            sss.set_light("light_torso","blue")
            sss.set_light("light_base","cyan")
            rospy.sleep(2)
            sss.set_light("light_torso","cyan")
            sss.set_mimic("mimic","happy")
            
            rospy.sleep(sleep_time)
            sss.set_mimic("mimic","falling_asleep",False)
            rospy.sleep(6)
            sss.set_mimic("mimic","sleeping")
            rospy.sleep(sleep_time)
            sss.set_mimic("mimic","waking_up",False)
            rospy.sleep(5)
            sss.set_mimic("mimic","happy")
            
            rospy.sleep(sleep_time)
            sss.set_mimic("mimic","confused")
            sss.set_light("light_base","yellow")
            rospy.sleep(2)
            sss.set_light("light_torso","yellow")
            sss.set_light("light_base","cyan")
            rospy.sleep(2)
            sss.set_light("light_torso","cyan")
            sss.set_mimic("mimic","happy")
            
            rospy.sleep(sleep_time)
            sss.set_mimic("mimic","blinking_right",False)
            rospy.sleep(2)
            sss.set_mimic("mimic","happy")
            rospy.sleep(sleep_time)
            sss.set_mimic("mimic","blinking_left",False)
            rospy.sleep(2)
            sss.set_mimic("mimic","happy")
            
            rospy.sleep(sleep_time)
            sss.set_mimic("mimic","tired")
            sss.set_light("light_base","green")
            rospy.sleep(2)
            sss.set_light("light_torso","green")
            sss.set_light("light_base","cyan")
            rospy.sleep(2)
            sss.set_light("light_torso","cyan")
            sss.set_mimic("mimic","happy")
            
            rospy.sleep(sleep_time)
            sss.set_mimic("mimic","laughing",False)
            rospy.sleep(6)
            sss.set_mimic("mimic","happy")
                                              
        return "succeeded"

## -- State Machine 

class Explore(smach.StateMachine):
    def __init__(self):
        smach.StateMachine.__init__(self,
            outcomes=['finished','failed'])
        with self:

#            smach.StateMachine.add('COB_COLORS_PREPARE',CobColorsPrepare(),
#                transitions={'succeeded':'COB_COLORS',
#                    'failed':'failed'})

            smach.StateMachine.add('COB_COLORS',CobColors(),
                transitions={'succeeded':'finished',
                    'failed':'failed'})

















class SM(smach.StateMachine):
    def __init__(self):
        smach.StateMachine.__init__(self,outcomes=['ended'])
        with self:
            smach.StateMachine.add('STATE',Explore(),
                transitions={'finished':'ended',
                    'failed':'ended'})

if __name__=='__main__':
    rospy.init_node('cob_colors')
    sm = SM()
    sis = smach_ros.IntrospectionServer('SM', sm, 'SM')
    sis.start()
    outcome = sm.execute()
    rospy.spin()
    sis.stop()
