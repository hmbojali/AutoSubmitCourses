import pyautogui
import time

def init():
    time.sleep(5)
    pyautogui.dragTo(300, 480)
    time.sleep(0.1)
    pyautogui.hscroll(2000)
    scroll_to_correct_cords = 700
    pyautogui.hscroll(-scroll_to_correct_cords)
#(600,535) green bar place
# pyautogui.dragTo(300,470)
# time.sleep(1)
#
# scroll_goal=700
# pyautogui.hscroll(-scroll_goal)

init()

scroll_distance = 113
for i in range(1,5):
    pyautogui.hscroll(-scroll_distance)
    time.sleep(0.2)

time.sleep(2)

for i in range(1,5):
    pyautogui.hscroll(scroll_distance)
    time.sleep(0.2)


print (pyautogui.KEYBOARD_KEYS)