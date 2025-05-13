import os.path
from time import sleep

import pyautogui
import cv2
import numpy as np
import time
import keyboard

# **@params:
scroll_distance = 113
num_of_courses = 1
wait_time = 3
start_time = time.time()
elapsed_time_file_path = "./PhilosophyOfTime&Space_elapsedTime.txt"
saved_time_delta = 0

total_time_elapsed = 0

def if_shut_down():
    if keyboard.is_pressed('num 0'):
        print("Shutting down the program.")
        print_time_elapsed()
        pyautogui.keyDown('alt')
        pyautogui.keyDown('tab')
        pyautogui.keyUp('alt')
        pyautogui.keyUp('tab')
        return True
    return False


def init():
    try:
        with open(elapsed_time_file_path, 'r') as f:
            global saved_time_delta
            saved_time_delta = int(float(f.readlines()[0].strip('\n')))
    except FileNotFoundError:
        with open(elapsed_time_file_path, 'w') as f:
            f.write(str(0))

def reset(sleep):
    start_time = time.time()

    time.sleep(sleep)
    pyautogui.dragTo(300, 480)
    time.sleep(0.1)
    pyautogui.hscroll(2000)
    scroll_to_correct_cords = 484
    pyautogui.hscroll(-scroll_to_correct_cords)
    time.sleep(0.1)



# Function to detect green on the screen
def detect_green():
    # taking a screenshot:
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # converting color to HSV color space:
    hsv_image = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)

    # defining the range for green color in HSV
    low_green = np.array([50, 70, 70])  # Adjust these values if necessary
    high_green = np.array([70, 255, 255])  # Adjust these values if necessary

    #a mask for the green areas
    mask = cv2.inRange(hsv_image, low_green, high_green)

    # Finding contours of the green areas
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # retunring true if green is detected
    return (len(contours) > 0), contours


def press_Esc():
    pyautogui.keyDown('esc')  # click esc after submitting
    time.sleep(0.1)
    pyautogui.keyUp('esc')  # click esc after submitting


# a function to click specific buttons on a website, in this case its submitting.
def click_buttons():
    pyautogui.click(300, 480)  # click הרשם למקצוע
    time.sleep(wait_time)  # wait for the page to load


def scroll_to_next():
    press_Esc()
    time.sleep(0.2)

    if not num_of_courses == 1:
        pyautogui.hscroll(-scroll_distance)  # scroll to next


def submit_course(contours):
    for contour in contours:
        if cv2.contourArea(contour) > 50:  # minimum size threshold
            x, y, w, h = cv2.boundingRect(contour)
            left_x = x + w
            center_y = y + h // 2

            group_offset_x = 725
            group_offset_y = -20

            click_x = left_x + group_offset_x
            click_y = center_y + group_offset_y

            pyautogui.click(click_x, click_y)  # click the group of course
            time.sleep(0.1)  # Sleep for a bit to avoid multiple clicks
            pyautogui.click(520, 950)  # Click submit
            time.sleep(5)  # Sleep for a bit for it to load
            press_Esc()  # click esc after submitting
            break



def main():
    # Infresete loop to actively watch the screen
    try:
        init()
        reset(5)
        while True:
            for i in range(0, num_of_courses):
                if if_shut_down():
                    return

                click_buttons()  # Regular button clicks when green isn't found

                if if_shut_down():
                    return

                # Detect green
                found_green, contours = detect_green()
                if found_green:
                    print("Green detected! Clicking alternate buttons...")
                    submit_course(contours)  # Click appropriate buttons when green is detected
                    contours = None
                    pyautogui.dragTo(300, 480)  # click הרשם למקצוע
                else:
                    print("No green detected. scrolling to next regular buttons...")

                time.sleep(0.1)
                scroll_to_next()

                if if_shut_down():
                    return

                time.sleep(0.2)  # Adjust this delay as needed

            global total_time_elapsed
            total_time_elapsed = time.time() - start_time + saved_time_delta
            with open(elapsed_time_file_path, 'w') as f:
                f.write(str(total_time_elapsed))

            reset(0.1)

    except KeyboardInterrupt:
        print("Program stopped by user.")
        print_time_elapsed()

def print_time_elapsed():
    print("total time elapsed: " + str(int(total_time_elapsed / 6) / 10.0) + 'min = ' + str(
        int(total_time_elapsed / 36) / 100.0) + 'h')


main()
