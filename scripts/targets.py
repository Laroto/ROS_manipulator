import tkinter as tk
from tkinter import ttk
import rospy
#from std_msgs.msg import Float32MultiArray
from neeeilit.msg import target

rospy.init_node('gui_publisher')
#pub = rospy.Publisher('/interface', Float32MultiArray, queue_size=10)
pub = rospy.Publisher('/arm_pos', target, queue_size=1)

# send position to the arm through ROS
def send_positions(sliders):
    rospy.loginfo("Sending positions to the arm")
    float_list = [slider.get() for slider in sliders]
    #msg = Float32MultiArray()
    msg = target()
    msg.x = float_list[0]
    msg.y = float_list[1]
    msg.z = float_list[2]
    msg.pitch = float_list[3]
    #msg.data = float_list
    pub.publish(msg)

# Create a Tkinter window
root = tk.Tk()
root.title("Robotic Arm Control")

# Define a style for the widgets
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12), foreground="#333")
style.configure("TButton", font=("Arial", 12),
                foreground="#fff", background="#0099cc")
style.configure("Horizontal.TScale", sliderthickness=20,
                troughcolor="#ccc", background="#fff", foreground="#0099cc")


labels = []
slides = []
etiquetas = ['x', 'y', 'z', 'pitch']

for i in range(3):
    #label = ttk.Label(root, text="DOF {}".format(i+1), style="TLabel")
    label = ttk.Label(root, text="{}".format(etiquetas[i]), style="TLabel")
    label.pack(padx=10, pady=10)
    labels.append(label)

    slider = ttk.Scale(root, from_=-0.30, to=0.30, orient="horizontal", length=400,
                        style="Horizontal.TScale", command=lambda x: print("Slider {}: {}".format(i+1, x)))
    slider.pack(padx=10, pady=10)
    slides.append(slider)  

#label = ttk.Label(root, text="DOF {}".format(i+1), style="TLabel")
label = ttk.Label(root, text="pitch".format(etiquetas[i]), style="TLabel")
label.pack(padx=10, pady=10)
labels.append(label)

slider = ttk.Scale(root, from_=-90, to=90, orient="horizontal", length=400,
                    style="Horizontal.TScale", command=lambda x: print("Slider {}: {}".format(i+1, x)), value=0)
slider.pack(padx=10, pady=10)
slides.append(slider) 

button = ttk.Button(root, text="Send", style="TButton", command=lambda: send_positions(slides))
button.pack(padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()
