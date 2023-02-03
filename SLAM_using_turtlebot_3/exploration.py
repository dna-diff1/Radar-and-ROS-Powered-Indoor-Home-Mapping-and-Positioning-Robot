#!/usr/bin/env python3
import rospy
import numpy as np
from sensor_msgs.msg import LaserScan 
from geometry_msgs.msg import Twist 
import roslaunch
import time
import random

dir_n = 1
count = 0
def callback(dt):
    global count 
    global dir_n
    fl = 0
    fr = 0 
    thr1 = 0.65
    thr2 = 0.45

    data = np.array(dt.ranges)

    front1 = []
    front = []
    side1 = []
    side =[]
    left = []
    right = []

    t1 = max(data[0:4])
    t2 = max(data[-5:])
    front1 = min(t1,t2)
    front.append(front1)
    t1 = max(data[5:9])
    t2 = max(data[10:14])
    front1 = min(t1,t2)
    front.append(front1)
    t1 = max(data[15:19])
    t2 = max(data[20:24])
    front1 = min(t1,t2)
    front.append(front1)
    t1 = max(data[-15:-11])
    t2 = max(data[-10:-4])
    front1 = min(t1,t2)
    front.append(front1)
    t1 = max(data[-25:-21])
    t2 = max(data[-20:-16])
    front1 = min(t1,t2)
    front.append(front1)
  
   
    t1 = max(data[25:29])
    t2 = max(data[30:34])
    side1 = min(t1,t2)
    left.append(side1)
    t1 = max(data[35:39])
    t2 = max(data[40:44])
    side1 = min(t1,t2)
    left.append(side1)
 
    side1 = min(t1,t2)
    left.append(side1)
    t1 = max(data[-35:-31])
    t2 = max(data[-30:-26])
    side1 = min(t1,t2)
    right.append(side1)
    t1 = max(data[-45:-41])
    t2 = max(data[-40:-36])
    side1 = min(t1,t2)
    right.append(side1)
  


    if min(front)>thr1:
        if count%2 == 0:
            move_forward_r()
            dir_n = 1
        else:
            move_forward_l()
            dir_n = 2
    else:
        if dir_n == 1:
            turn_left()
            count = count + 1
        elif dir_n == 2:
            turn_right()
            count = count + 1
          

def save_map():
  package = 'map_server'
  type = 'map_saver'
  node = roslaunch.core.Node(package, type, args="-f $(find acs6121_team4)/maps/explore_map")
  launch = roslaunch.scriptapi.ROSLaunch()
  launch.start()
  task = launch.launch(node)


def move_forward_l():
    vel.linear.x = 0.4
    vel.angular.z = 0.5
    pub.publish(vel)
def move_forward_r():
    vel.linear.x = 0.4
    vel.angular.z = -0.5
    pub.publish(vel)
def turn_left():
    vel.linear.x = 0.0
    vel.angular.z = 0.5
    pub.publish(vel)
def turn_right():
    vel.linear.x = 0.0
    vel.angular.z = -0.5
    pub.publish(vel)


   
vel = Twist() 
rospy.init_node('obstacle_avoidance_node')
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10) 
sub = rospy.Subscriber("/scan", LaserScan, callback) 
      

def main():
  while not rospy.is_shutdown():
    save_map() 


if __name__ == '__main__':
    try:
      main()
    except rospy.ROSInterruptException:
        pass