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

##
#Missing in simulation:
#Movement of the base: sss.move_base_rel("base", [0.1[m], 0.1[m], 0.1[rad]], True)

## -- Initiation
class CobIntroductionInit(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
            outcomes=['succeeded','failed'])
			
    def execute(self, userdata):
        handle_base = sss.init("base")
        handle_arm_left = sss.init("arm_left")
        handle_arm_right = sss.init("arm_right")
        #handle_sensorring = sss.init("sensorring")

        if handle_base.get_error_code() != 0:
            return "failed"
        if handle_arm_left.get_error_code() != 0:
            return "failed"
        if handle_arm_right.get_error_code() != 0:
            return "failed"
        #if handle_sensorring.get_error_code() != 0:
            #return "failed"

        return "succeeded"
## -- Recover
class CobIntroductionRecover(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
            outcomes=['succeeded','failed'])
			
    def execute(self, userdata):
        handle_base = sss.recover("base")
        handle_arm_left = sss.recover("arm_left")
        handle_arm_right = sss.recover("arm_right")
        #handle_sensorring = sss.recover("sensorring")

        if handle_base.get_error_code() != 0:
            return "failed"
        if handle_arm_left.get_error_code() != 0:
            return "failed"
        if handle_arm_right.get_error_code() != 0:
            return "failed"
        #if handle_sensorring.get_error_code() != 0:
            #return "failed"

        return "succeeded"

## -- Prepare
class CobIntroductionPrepare(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
            outcomes=['succeeded','failed'])
			
    def execute(self, userdata):
        handle_arm_left = sss.move("arm_left", "folded",False)
        handle_arm_right = sss.move("arm_right", "folded",False)
        #handle_sensorring = sss.move("sensorring", "front",False)

        handle_arm_left.wait()
        handle_arm_right.wait()
        #handle_sensorring.wait()

        if handle_arm_left.get_error_code() != 0:
            return "failed"
        if handle_arm_right.get_error_code() != 0:
            return "failed"
        #if handle_sensorring.get_error_code() != 0:
            r#eturn "failed"

        return "succeeded"

## -- main script
class CobIntroduction(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
            outcomes=['succeeded','failed'])
			
    def execute(self, userdata):
        
        # :: Menue to select scenes
        while True:
            rospy.loginfo("------ Menu ------")
            rospy.loginfo("0 = Introduction & lights, mimics")
            rospy.loginfo("1 = Modules: base")
            rospy.loginfo("2 = Modules: torso")
            rospy.loginfo("3 = Modules: arms")
            rospy.loginfo("4 = Modules: head")
            rospy.loginfo("5 = Software highlights")
            while True:
                try:          
                    #usr_input = raw_input("Please type a number(int) for the scene to begin with:")
                    #n = int(usr_input)
                    n=0
                    break
                except ValueError:
                    rospy.loginfo("You didn't type a number, please try again")
            break
		
        if n == 0:
            # :: 0.Introduction & lights
            sss.set_mimic("mimic","happy")
            rospy.loginfo("Beginning introduction of Care-O-Bot 4-2 for HMI 2015")
            sss.move("arm_right", "side", False)
            sss.move("arm_left", "side")

            rospy.loginfo("Hello and Welcome")
            sss.say(["Hello and welcome to my presentation, my name is Care o bot. I'm a mobile service robot build by Fraunhofer I. P. A., in Stuttgart. Don't be afraid, i am a gentleman"], False)
            wave_right_handle = sss.move("arm_right", "wave_hmi", False)
            sss.move_base_rel("base", [0, 0, -0.78], False)
            
            sss.say(["I have a wide range of services. I can assist you at home or serve food and drinks in restaurants or hotels. In hospitals or care facilities I can support in various delivery tasks. Or i could work in a manufacturing enviroment shelf-picking and commissioning"], False)
            rospy.sleep(1)
            wave_right_handle.wait()
            sss.move_base_rel("base", [0, 0, 1.57], False)
            sss.move("arm_left", "wave_hmi", False)
            rospy.sleep(1)
            sss.move_base_rel("base", [0, 0, -0.78], False)
            
            
            #TODO show renderings on head display while explaining application domanis
            #sys.exit()

                        # Explain lights & display
            rospy.loginfo("Showing lights & mimis")
            point2chest_handle = sss.move("arm_right","point2chest", False)
            sss.say(["For interaction with you and expressing my mood i am able to change my colored lights and use my head-integrated display"], False)
            point2chest_handle.wait()
            sss.move("arm_right","side", False)
            sss.set_mimic("mimic",["laughing",0,3])
            sss.set_light("light_base", "cyan", False)
            sss.set_light("light_torso", "cyan")
            sss.say(["This is my normal color, showing you that i am ready to accept commands and orders"])
            sss.set_light("light_base","yellow", False)
            sss.set_light("light_torso","yellow")
            sss.set_mimic("mimic", ["busy",0,3])
            sss.say(["If you see me like this, you should pay attention to my movements, yellow means i am doing something"])
            sss.set_light("light_base","red", False)
            sss.set_light("light_torso","red")
            sss.set_mimic("mimic", ["confused",0,3])
            sss.say(["Red, of course, means there is an error happening. Dont worry, i feel good right now, this is only to show you my colors. I hope you will never see me like this"])
            sss.say(["This blue means i am thinking and calculation on how to help you the best"], False)
            sss.set_light("light_base","blue", False)
            sss.set_light("light_torso","blue")
            sss.say(["Now i'll turn back to my normal color, this is how i feel most comfortable"])
            sss.set_mimic("mimic","happy")
            sss.set_light("light_base","cyan", False)
            sss.set_light("light_torso","cyan")


            sss.say(["One of my technical highlights, is the modularity. Let me explain my different modules."])        
            			
            n = n+1

        if n == 1: 
            # :: 1.Explaing modules(base)
            rospy.loginfo("Explaining modules(base)")       
            sss.say(["I consist of 4 elementary parts: base, torso, arms and head, i'll start with my base."], False)
            sss.set_light("light_torso", "yellow")
            sss.move("arm_right", "point2base")
            sss.set_light("light_torso", "cyan")
            sss.set_light("light_base","yellow")
            sss.say(["I can move forward and backward"], False)
            sss.move_base_rel("base", [-0.1, 0, 0])
            sss.move_base_rel("base", [0.1, 0, 0])
            sss.say(["or sideways"])
            sss.move_base_rel("base", [0, 0.1, 0])
            sss.move_base_rel("base", [0, -0.1, 0])
            sss.move_base_rel("base", [0, -0.1, 0], False)
            sss.say(["and back."], False)
            sss.move_base_rel("base", [0, 0.1, 0])
            sss.say(["I am also capable to turn on the spot like this"])
            sss.move_base_rel("base", [0, 0, 0.5])
            sss.move_base_rel("base", [0, 0, 0.5])
            sss.move_base_rel("base", [0, 0, -0.5])
            sss.move_base_rel("base", [0, 0, -0.5])
            sss.move_base_rel("base", [0, 0, -0.5])
            sss.move_base_rel("base", [0, 0, 0.5])
            sss.set_light("light_base", "cyan")
            sss.say(["And, of course, i can combine the movements"])
            sss.say(["Using my safety laser scanners in the base I can safely navigate between humans."])  

            n = n+1
        
        if n == 2:
            # :: 2.Explain modules (torso)
            rospy.loginfo("Explaining modules(torso)")
            sss.set_light("light_base", "yellow")
            sss.move("arm_right","point2chest")
            sss.move("arm_right","draw_torso", False)
            sss.say(["The next module is my torso, you have already seen the lights i can change and use to interact with you"])
            sss.move("arm_right","point2camera")
            sss.say(["Here i have 3d cameras helping me to navigate and recognize obstacles "])
            sss.set_light("light_base","cyan")

            n = n+1
        
        if n == 3:
			# :: 3.Explain modules (arms)
            rospy.loginfo("Explaining modules(arms)")
            sss.set_light("light_base","yellow")
            sss.set_light("light_torso","yellow")
            sss.move("arm_right","side", False)
            sss.move("arm_left", "side")
            sss.say(["as you can see, i have two arms. I can use them independently."], False)
            sss.move("arm_right",[[0.9599, 1.4, -1.0472, -1.6581, -1.0472, -0.6981, 1.07]], False)
            sss.move("arm_left",[[-0.9599, -1.4, 1.0472, 1.6581, 1.0472, 0.6981, -1.07]]) 
            sss.move("arm_right",[[2, 1.4, -1.0472, -1.6581, -1.0472, -0.6981, 1.07]], False)  
            sss.move("arm_left",[[-2, -1.4, 1.0472, 1.6581, 1.0472, 0.6981, -1.07]])
            sss.move("arm_right",[[0.5, 1.4, -1.0472, -1.6581, -1.0472, -0.6981, 1.07]], False)    
            sss.move("arm_left",[[-0.5, -1.4, 1.0472, 1.6581, 1.0472, 0.6981, -1.07]])
            
            sss.say(["Both arms consist of 7 independent joints, allowing me to perform complex movements"], False)
            # Folded arm_right: [[0.9599, 1.5708, -0.12, 1.0, 1.38, 0.75, -1.36]]
            sss.move("arm_right","folded",False)
            sss.move("arm_left","folded")
            # Reverse folded
            sss.move("arm_right", [[-0.9599, -1.5708, 0.12, -1.0, -1.38, -0.75, 1.36]], False)
            sss.move("arm_left", [[0.9599, 1.5708, -0.12, 1.0, 1.38, 0.75, -1.36]])
            # End Reverse folded
            sss.move("arm_right", "side", False)
            sss.move("arm_right", "side")
            sss.set_light("light_base","cyan")
            sss.set_light("light_torso","cyan")
            # :: 3.1.Hands
            #sss.move("arm_right", "carry", False)
            #sss.move("arm_left", "carry", False)
            sss.say(["Not only do i have arms, but also hands."])
            ## Open , close hands
            sss.move("gripper_right","open")
            sss.move("gripper_left","open")
            sss.say(["Combined with my 3D-Sensors i am able to recognize objects and grab or manipulate them"])
            sss.move("gripper_right","closed")
            sss.move("gripper_left","closed")
            sss.say(["So i could not only entertain you, but actually help you carry stuff around in your apartment"])		
            
            sss.move("arm_right", "side", False)
            sss.move("arm_left", "folded")
            
            n = n+1

        if n == 4:
            # :: 4.Explain modules(head)
            rospy.loginfo("Explaining modules(head)")
            sss.set_light("light_torso","yellow")
            sss.move("arm_right", "point2head", False)
            sss.set_light("light_torso","cyan")
            sss.say(["And finally, something i always forget, my head"])
            sss.set_mimic("mimic",["surprised",0,3])
            sss.move("arm_right", "side")
            sss.set_mimic("mimic","happy")
            sss.say(["To detect objects and recognize people i can move my sensor ring"])
            sss.move("sensorring","left")
            sss.move("sensorring","right")
            sss.move("sensorring","front")

        if n == 5:
            # :: 5.Software highlights
            #sss.move("arm_right", "open", False)
            #sss.move("arm_left", "open", False)
            sss.say(["Now that you have seen my hardware highlights, ill tell you something about my software"])
            sss.set_mimic("mimic",["blinking_right",0,2])
            sss.say(["I am shipped with open source drivers and powered by the Open Source Robot Operating System"])            
            
        ## :: Final
        rospy.loginfo("Final/Exit scene reached")
        sss.say(["Now, my presentation has finally come to and end"])
        sss.say(["Thank you for your intereset"])
        sss.move_base_rel("base", [0, 0, 0.5])
        sss.say(["Thank you"])
        sss.move_base_rel("base", [0, 0, -1], False)
        sss.say(["Thank you for your attention"])
        sss.move_base_rel("base", [0, 0, 0.5])

        #Menu to select finishing action
        rospy.loginfo("------ Menu for exit scenes ------")
        rospy.loginfo("!!!DEPENTS FROM ENVIROMENT - BE CAREFUL!!!")
        rospy.loginfo("0 = arms folded")
        rospy.loginfo("1 = get cookies(HMI-2015)")
        while True:
            try:
                user_input=raw_input("Please select how to finish the presentation:")
                i=int(user_input)
                break
            except ValueError:
                rospy.loginfo("You didn't type a number, please try again")

        if i == 0:
            #Arms folded
            sss.move("arm_left", "folded", False)
            sss.move("arm_right", "folded")

        if i == 1:
            ## Find cookies, bring them to the viewers
            pass

        return "succeeded"

## -- State Machine 

class Explore(smach.StateMachine):
    def __init__(self):
        smach.StateMachine.__init__(self,
            outcomes=['finished','failed'])
        with self:

#            smach.StateMachine.add('COB_INTRODUCTION_PREPARE',CobIntroductionPrepare(),
#                transitions={'succeeded':'COB_INTRODUCTION',
#                    'failed':'failed'})

            smach.StateMachine.add('COB_INTRODUCTION',CobIntroduction(),
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
    rospy.init_node('cob_introduction')
    sm = SM()
    sis = smach_ros.IntrospectionServer('SM', sm, 'SM')
    sis.start()
    outcome = sm.execute()
    rospy.spin()
    sis.stop()
