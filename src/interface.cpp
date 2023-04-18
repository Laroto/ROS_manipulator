#include <iostream>
#include <fcntl.h>
#include <termios.h>
#include <unistd.h>

#include <ros/ros.h>
#include "neeeilit/arm_pos.h"

//neeeilit::arm_pos in_msg;

class Servo {
    public:
        Servo(int min, int max, int offset);
        void setAngle(int angle);
        float getAngle() { return angle; }
    
    private:
        int min;
        int max;
        int offset;
        int angle = 90;
};

Servo::Servo(int pin, int max, int offset) {
    this->min = min;
    this->max = max;
    this->offset = offset;
}

void Servo::setAngle(int angle) {
    this->angle = angle + offset;
}

void send_servos_serial(int fd, Servo servos[], int num_servos) {
    float angle;
    for (int i = 0; i < num_servos; i++) {
        angle = servos[i].getAngle();
        write(fd, &angle, sizeof(float));
    }
}

Servo servos[5] = {
        Servo(0, 180, 10),
        Servo(0, 180, 15),
        Servo(0, 180, 20),
        Servo(0, 180, 75),
        Servo(0, 180, 0)
    };

void callback(const neeeilit::arm_pos::ConstPtr& msg)
{
    //in_msg = *msg;
    //ROS_INFO("I heard: [%f]", msg->x);
    servos[0].setAngle(msg->joint1);
    servos[1].setAngle(msg->joint2);
    servos[2].setAngle(msg->joint3);
    servos[3].setAngle(msg->joint4);
    servos[4].setAngle(msg->gripper);

    std::cout << "  Servo 1: " << servos[0].getAngle();
    std::cout << "  Servo 2: " << servos[1].getAngle();
    std::cout << "  Servo 3: " << servos[2].getAngle();
    std::cout << "  Servo 4: " << servos[3].getAngle();
    std::cout << "  Servo 5: " << servos[4].getAngle() << std::endl;
}

int main(int argc, char **argv)
{
    
    ros::init(argc, argv, "interface");

    ros::NodeHandle n;

    std::string port; 

    n.param<std::string>("port", port, "/dev/ttyACM1");

    std::cout << "Port: " << port << std::endl;

    ros::Subscriber sub = n.subscribe("/interface", 1, callback);

    char *porta = &port[0];
    int fd = open(porta, O_RDWR | O_NOCTTY);

    if (fd == -1)
    {
        ROS_ERROR("Error opening serial port!");
        return -1;
    }

    struct termios serial;
    tcgetattr(fd, &serial);

    serial.c_cflag = B9600 | CS8 | CLOCAL | CREAD;
    serial.c_iflag = 0;
    serial.c_oflag = 0;
    serial.c_lflag = 0;

    tcsetattr(fd, TCSANOW, &serial);
    
    send_servos_serial(fd, servos, 5);

    ros::Rate rate(10);

    ROS_WARN("Interface node started");

    while (ros::ok())
    {
        rate.sleep();
        ros::spinOnce();
        send_servos_serial(fd, servos, 5);
    }

    close(fd);

    return 0;
}