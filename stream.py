from PIL import ImageGrab
import numpy as np
import cv2
from pynput.keyboard import Key, Controller
keyboard = Controller()

from threading import Thread
from queue import Queue
import time, pyautogui

q = Queue()
enable = False
def keyboard_event(queue):
    import time
    global enable
    def hold_space (hold_time):
        start = time.time()
        while time.time() - start < hold_time:
            pyautogui.press(' ')
    while True:
        if not queue.empty():
            sig = queue.get()

            keyboard.press(Key.space)
            #cv2.waitKey(500)
            time.sleep(0.3)
            keyboard.release(Key.space)
            enable = True
            #half a second
            print("Cactus - detected => JUMP!")
            #hold_space(0.5)



t = Thread(target=keyboard_event, args=(q,))
t.daemon = True
t.start()


while(True):
    img = ImageGrab.grab(bbox=(80,10,500,280)) #bbox specifies specific region (bbox= x,y,width,height)
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    # Otsu's thresholding
    frame = 1 - frame
    y = 218
    h = 40
    x = 125
    w = 30

    ret2, th2 = cv2.threshold(frame,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    frame = th2[y:y + h, x:x + w]

    cntNotBlack = cv2.countNonZero(frame)
    if cv2.waitKey(1) == ord('e'):
        enable = not enable
        print('enabled')
    if cntNotBlack > 100 and enable:
        #pyautogui.keyDown(' ')
        #time.sleep(1)
        #pyautogui.keyUp(' ')
        q.put(True)
        enable = False
        print(cntNotBlack)
    #else:
        #keyboard.release(Key.space)


    cv2.imshow("Cactus Detector", frame)
    cv2.imshow("Screen Streamer", th2)
    cv2.waitKey(1)
cv2.destroyAllWindows()
