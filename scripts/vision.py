import cv2
import mediapipe as mp
import rospy
from neeeilit.msg import target

rospy.init_node('vision')
pub = rospy.Publisher('/arm_pos', target, queue_size=1)

class handTracker():
    def __init__(self, mode=False, maxHands=1, detectionCon=0.5, modelComplexity=1, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def handsFinder(self, image, draw=True):
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image

    def positionFinder(self, image, handNo=0, draw=8):
        sp_lmlist = []

        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[handNo]
            sp_lmlist = Hand.landmark
            #wp_lmlist = Hand.world_landmark
            if draw != None:
                h, w, c = image.shape
                lm = sp_lmlist[draw]
                cx, cy = int(lm.x*w), int(lm.y*h)
                cv2.circle(image, (cx, cy), 9,
                           (255, 0, 255), cv2.FILLED)
                
                # cv2.circle(image, (cx, cy), 5,
                #            (0, 255, 0), cv2.FILLED)
                # cv2.circle(image, (cx, cy), 17,
                #            (0, 255, 0), cv2.FILLED)
                
                
                           
                

        return sp_lmlist

def distanceCalculate(p1, p2):
    """p1 and p2 in format (x1,y1) and (x2,y2) tuples"""
    dis = ((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2) ** 0.5
    return dis

def main():
    cap = cv2.VideoCapture(0) # 0 para camara do pc e 4 para camara usb
    tracker = handTracker()

    cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        success, image = cap.read()
        image = cv2.flip(image,1)
        image = tracker.handsFinder(image)
        sp = tracker.positionFinder(image)
        if len(sp) != 0:
            print(sp[8])
        
            msg = target()
            msg.x = 0.2
            msg.y = (sp[8].x - 0.5) * 0.4
            msg.z = (1-sp[8].y) * 0.18

            dist = distanceCalculate(sp[4], sp[16])
            print (dist)

            

            if dist < 0.05:
                msg.gripper = 0
            else:
                msg.gripper = 90

            pub.publish(msg)

        #cv2.namedWindow("video", cv2.WND_PROP_FULLSCREEN)
        #cv2.setWindowProperty("video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
        cv2.imshow("Video", image)
        if (cv2.waitKey(1) & 0x7F == ord('q')):
            print("Exit requested")
            break


if __name__ == "__main__":
    main()
