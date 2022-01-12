import cv2
from cvzone.HandTrackingModule import HandDetector


class Button:
    def __init__(self, pos, width, height, val):
        self.pos = pos
        self.width = width
        self.height = height
        self.val = val

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height), (0,165,255), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height), (50, 50, 50), 3)
        cv2.putText(img, self.val, (self.pos[0] + 40, self.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN, 2,  (0,0,0), 2)

    def onClickListener(self, x, y):
        #x1 < x < x2
        if((self.pos[0] < x < self.pos[0] + self.width) and (self.pos[1] < y < self.pos[1] + self.height)):
            cv2.rectangle(img, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height), (255, 255, 255), cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height), (0,0,0), 3)
            cv2.putText(img, self.val, (self.pos[0] + 25, self.pos[1] + 80), cv2.FONT_HERSHEY_PLAIN, 5, (0,0,0), 5)
            return True
        else:
            return False


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=1)

b_values = [['7', '8', '9', '*'], ['4', '5', '6', '-'], ['1', '2', '3', '+'], ['0', '.', '/', '=']]

buttons = []
for x in range(4):
    for y in range(4):
        xpos = (x * 100) + 800
        ypos = (y * 100) + 150
        buttons.append(Button((xpos, ypos), 100, 100, b_values[y][x]))

eqn = ''
delay_counter = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img, flipType=False)
    
    cv2.rectangle(img, (800, 50), (800 + 400, 70 + 100), (0,0,0), cv2.FILLED)
    cv2.rectangle(img, (800, 50), (800 + 400, 70 + 100), (0,0,0), 3)

    for button in buttons:
        button.draw(img)

    if hands:
        lmList = hands[0]['lmList']
        length, _, img = detector.findDistance(lmList[8], lmList[12], img)
        # print(length)
        x, y = lmList[8]
        if(length < 50):
            for count, button in enumerate(buttons):
                if(button.onClickListener(x, y)) and delay_counter == 0:
                    entered_eqn = b_values[int(count % 4)][int(count / 4)]
                    if(entered_eqn == "="):
                        eqn = str("{:.2f}".format(eval(eqn)))
                    else:
                        eqn += entered_eqn
                    delay_counter = 1
    if(delay_counter != 0):
        delay_counter += 1
        if(delay_counter > 10):
            delay_counter = 0
        
    cv2.putText(img, eqn, (810, 120), cv2.FONT_HERSHEY_PLAIN, 3, (0, 165, 255), 3)
    
    cv2.imshow("Img", img)
    k = cv2.waitKey(1)
    if(k == ord('c')):
        eqn = ''
    if (k==27):
        break
cv2.destroyAllWindows()

  