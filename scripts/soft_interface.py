#!/usr/bin/env python

import sys
import rospy
import moveit_commander
from moveit_msgs.msg import DisplayTrajectory

# Initialize the moveit_commander and rospy
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('moveit_arm_controller', anonymous=True)

# Instantiate a RobotCommander object
robot = moveit_commander.RobotCommander()

# Instantiate a PlanningSceneInterface object
scene = moveit_commander.PlanningSceneInterface()

# Instantiate a MoveGroupCommander object for the arm
arm_group = moveit_commander.MoveGroupCommander('arm_group')

# Set the planner to use the RRTConnect algorithm
arm_group.set_planner_id('RRTConnectkConfigDefault')

# Set the reference frame
arm_group.set_pose_reference_frame('base_link')

# Set the end effector link
arm_group.set_end_effector_link('joint3_to_joint4')

# Allow replanning to increase the odds of a solution
arm_group.allow_replanning(True)

# Set the planning time
arm_group.set_planning_time(1.0)

# Create a publisher for the DisplayTrajectory topic
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', DisplayTrajectory, queue_size=10)

# Move the arm to a named pose
arm_group.set_named_target('pose1')
plan_home = arm_group.go(wait=True)

# Publish the trajectory to Rviz
display_trajectory = DisplayTrajectory()
display_trajectory.trajectory_start = robot.get_current_state()
display_trajectory.trajectory.append(plan_home)
display_trajectory_publisher.publish(display_trajectory)

# Move the arm to a new pose
arm_group.set_position_target([0.2, 0.0, 0.2])
plan_target = arm_group.go(wait=True)

# Publish the trajectory to Rviz
display_trajectory = DisplayTrajectory()
display_trajectory.trajectory_start = robot.get_current_state()
display_trajectory.trajectory.append(plan_target)
display_trajectory_publisher.publish(display_trajectory)

# Shutdown the moveit_commander and rospy
moveit_commander.roscpp_shutdown()
rospy.signal_shutdown("Done!")