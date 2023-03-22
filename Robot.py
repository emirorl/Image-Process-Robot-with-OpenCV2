import time
import numpy as np
import cv2
from picamera2 import MappedArray, Picamera2, Preview
from picamera2.encoders import H264Encoder
from PIL import Image, ImageFilter 
import RPi.GPIO as GPIO
import time

global puan
puan = 0
global y_cntrl
y_cntrl = 0
global y_cntrl2
y_cntrl2 = 0
global temp_puan
temp_puan = 0
def motorfonk(kordinat):

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    hiz = 36
    IN1=20
    IN2=21
    ENA=16
    IN3 = 26
    IN4 = 19
    GPIO.setup(IN1,GPIO.OUT)
    GPIO.setup(IN2,GPIO.OUT)
    GPIO.setup(IN3,GPIO.OUT)
    GPIO.setup(IN4,GPIO.OUT)
    GPIO.setup(ENA,GPIO.OUT)
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.LOW)

    p=GPIO.PWM(ENA,1000)
    
    p.start(0)

    def geri(hiz):
        GPIO.output(IN1,GPIO.HIGH)
        GPIO.output(IN4,GPIO.HIGH)
        GPIO.output(IN2,GPIO.LOW)
        GPIO.output(IN3,GPIO.LOW)
        p.ChangeDutyCycle(hiz)

    def ileri(hiz):
        GPIO.output(IN1,GPIO.LOW)
        GPIO.output(IN4,GPIO.LOW)
        GPIO.output(IN2,GPIO.HIGH)
        GPIO.output(IN3,GPIO.HIGH)
        p.ChangeDutyCycle(hiz)

    def dur():
        GPIO.output(IN1,GPIO.LOW)
        GPIO.output(IN2,GPIO.LOW)
        GPIO.output(IN3,GPIO.LOW)
        GPIO.output(IN4,GPIO.LOW)
        p.ChangeDutyCycle(0)
        
    if kordinat < 310:
        geri(hiz)
        time.sleep(0.1)
        
    elif kordinat > 340:
        ileri(hiz)
        time.sleep(0.1)
            
    elif  310 < kordinat  and kordinat < 340:
        dur()
        time.sleep(0.4)        
    
    

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format":'XRGB8888',"size":(640, 480)}))
picam2.start()


while(1):
    with open("/sys/class/gpio/gpio5/value") as pin:
        status = pin.read(5)
    
    green_processed = False #Variable to check if the first green area has been processed
    red_processed = False # Variable to check if the red area has ben processed
    imageFrame = picam2.capture_array()

    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    red_lower = np.array([149, 0, 208], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
    
    green_lower = np.array([69, 230, 175], np.uint8)
    green_upper = np.array([104, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

    kernal = np.ones((5, 5), "uint8")
    
    red_mask = cv2.dilate(red_mask, kernal)
    res_red = cv2.bitwise_and(imageFrame, imageFrame, mask = red_mask)
    
    green_mask = cv2.dilate(green_mask, kernal)
    res_green = cv2.bitwise_and(imageFrame, imageFrame, mask = green_mask)


    kirmizi_x = 0
    kirmizi_y = 0
    yesil_x = 0
    yesil_y = 0
    temp_y = 0
    if int(status)==1:
        contours_green, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contours_green in enumerate(contours_green):
            area = cv2.contourArea(contours_green)
            if(area > 150):
                x, y, w, h = cv2.boundingRect(contours_green)
                yesil_mid_bottom_coordinate = (x+w/2,y+h)
                yesil_x = yesil_mid_bottom_coordinate[0]
                temp_y = y_cntrl
                yesil_y = yesil_mid_bottom_coordinate[1]
                y_cntrl = yesil_y
                imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h),(0, 255, 0), 2)
                cv2.putText(imageFrame, "Green Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX,  1.0, (0, 255, 0))
                if yesil_mid_bottom_coordinate[1] > 330:
                    if not green_processed: # Check if the first green area has been processed
                        motorfonk(yesil_mid_bottom_coordinate[0])
                        green_processed = True # Mark the first green area as processed to ignore additional green areas

                if ((yesil_mid_bottom_coordinate[0]>305 and yesil_mid_bottom_coordinate[0]<345) and yesil_mid_bottom_coordinate[1] > 360):
                    puan+=0.270
                if(int(puan)%2==0 and int(temp_puan)!=int(puan)):
                    print('Puanınız = ', int(puan))
                    temp_puan= int(puan)
                elif(temp_puan!= int(puan)):
                    puan+=1
                    temp_puan =int(puan)
                    print('Puanınız = ', int(puan))
        if(yesil_x==0 and yesil_y==0):
            contours_red, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for pic, contours_red in enumerate(contours_red):
                area = cv2.contourArea(contours_red)
                if(area > 150):
                    x, y, w, h = cv2.boundingRect(contours_red)
                    kirmizi_mid_bottom_coordinate = (x+w/2,y+h)
                    kirmizi_x = kirmizi_mid_bottom_coordinate[0]
                    kirmizi_y = kirmizi_mid_bottom_coordinate[1]
                    imageFrame = cv2.rectangle(imageFrame, (x, y),(x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(imageFrame, "Red Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0,(0, 0, 255))
                    if (kirmizi_x > 200 and kirmizi_x < 400):
                        motorfonk(100)
                        time.sleep(0.5)
                        motorfonk(400)
                        time.sleep(0.5)
                        GPIO.cleanup()
    if int(status)==0:
        contours_red, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contours_red in enumerate(contours_red):
            area = cv2.contourArea(contours_red)
            if(area > 130):
                x, y, w, h = cv2.boundingRect(contours_red)
                kirmizi_mid_bottom_coordinate = (x+w/2,y+h)
                kirmizi_x = kirmizi_mid_bottom_coordinate[0]
                temp_y = y_cntrl2
                kirmizi_y = kirmizi_mid_bottom_coordinate[1]
                y_cntrl2 = kirmizi_y
                imageFrame = cv2.rectangle(imageFrame, (x, y),(x + w, y + h), (0, 0, 255), 2)
                cv2.putText(imageFrame, "Red Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0,(0, 0, 255))
                if kirmizi_mid_bottom_coordinate[1] > 330:
                    if not red_processed:
                        motorfonk(kirmizi_mid_bottom_coordinate[0])
                        red_processed = True
                if ((kirmizi_mid_bottom_coordinate[0]>305 and kirmizi_mid_bottom_coordinate[0]<345) and kirmizi_mid_bottom_coordinate[1] > 345):
                    puan+=0.25
                if(int(puan)%2==0 and int(temp_puan!= int(puan))):
                    print('Puanınız = ', int(puan))
                    temp_puan= int(puan)
                elif(temp_puan!= int(puan)):
                    puan+=1
                    temp_puan= int(puan)
                    print('Puanınız = ', int(puan))
        if(kirmizi_x==0 and kirmizi_y==0):
            contours_green, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for pic, contours_green in enumerate(contours_green):
                area = cv2.contourArea(contours_green)
                if(area > 150):
                    x, y, w, h = cv2.boundingRect(contours_green)
                    yesil_mid_bottom_coordinate = (x+w/2,y+h)
                    yesil_x = yesil_mid_bottom_coordinate[0]
                    yesil_y = yesil_mid_bottom_coordinate[1]
                    imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h),(0, 255, 0), 2)
                    cv2.putText(imageFrame, "Green Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX,  1.0, (0, 255, 0))
                    if (yesil_x > 280 and yesil_y < 320):
                        motorfonk(100)
                        time.sleep(0.5)
                        motorfonk(400)
                        time.sleep(0.5)
                        GPIO.cleanup()
    cv2.imshow("Color Detection", imageFrame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break