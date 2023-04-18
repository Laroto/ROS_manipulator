#include <ros/ros.h>
#include "neeeilit/arm_pos.h"
#include "neeeilit/target.h"

neeeilit::arm_pos out_msg;

ros::Publisher pub;

void callback(const neeeilit::target::ConstPtr& msg)
{
    // float a3 = 0.135;
    // float a4 = 0.095;
    // compute inverse kinematics for 4 DOF robot arm with a gripper
    // and publish the joint angles to the arm_pos topic
    
    float l1 = 0.095;
    float l2 = 0.133;
    float l3 = 0.092;
    float l4 = 0.135;
    //float phi = 0;

    // if((msg->x*msg->x + msg->y*msg->y + msg->z*msg->z  > 0.35*0.35) || (msg->x*msg->x + msg->y*msg->y + msg->z*msg->z  < l4*l4 ) || msg->x < 0 || msg->z < 0 )
    // {
    //     ROS_ERROR("Target out of reach");
    //     return;
    // }

    out_msg.joint1 = atan2(msg->y, msg->x) + M_PI/2;

    // convert cartesian to cilindrical coordinates
    float r = sqrt(msg->x*msg->x + msg->y*msg->y);
    float theta = atan2(msg->y, msg->x);
    float z = msg->z;

    float z_ = z + l4 * sin(msg->pitch*M_PI/180);
    float r_ = r - l4 * cos(msg->pitch*M_PI/180);

    // float d = sqrt(r*r + z*z);
    // float alpha2 = acos((d*d - l2*l2 - l3*l3)/(-2*l2*l3));
    // out_msg.joint3 = M_PI - alpha2;

    float d = sqrt(r_*r_ + z_*z_);
    float alpha2 = acos((d*d - l2*l2 - l3*l3)/(-2*l2*l3));
    out_msg.joint3 = M_PI - alpha2;

    // float alpha3 = atan2(z, r);
    // out_msg.joint2 = alpha3 + acos((l3*l3 - l2*l2 - d*d)/(-2*l2*d));

    float alpha3 = atan2(z_, r_);
    out_msg.joint2 = alpha3 + acos((l3*l3 - l2*l2 - d*d)/(-2*l2*d));

    out_msg.joint4 = out_msg.joint2 - out_msg.joint3 + msg->pitch*M_PI/180;


    // convert radians to degrees
    // out_msg.joint4 = 0;
    out_msg.joint1 *= 180 / M_PI;
    out_msg.joint2 *= 180 / M_PI;
    out_msg.joint3 *= 180 / M_PI;
    out_msg.joint4 *= 180 / M_PI;

    if (isnanf(out_msg.joint1) || isnanf(out_msg.joint2) || isnanf(out_msg.joint3) || isnanf(out_msg.joint4))
    {
        if (isnanf(out_msg.joint1))
            ROS_ERROR("joint 1 ");

        if (isnanf(out_msg.joint2))
            ROS_ERROR("joint2 ");

        if (isnanf(out_msg.joint3))
            ROS_ERROR("joint3 ");

        if (isnanf(out_msg.joint4))
            ROS_ERROR("joint4 ");

        ROS_ERROR("NAN");
        return;
    }

    pub.publish(out_msg);
}

int main(int argc, char **argv)
{
    
    ros::init(argc, argv, "inverse");

    ros::NodeHandle n;

    pub = n.advertise<neeeilit::arm_pos>("/interface", 1);
    ros::Subscriber sub = n.subscribe("/arm_pos", 1, callback);

    ros::Rate rate(100);

    while(ros::ok())
    {
        ros::spinOnce();
        rate.sleep();
   }
}