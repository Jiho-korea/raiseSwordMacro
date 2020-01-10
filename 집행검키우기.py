import pyautogui as pag
import mss
import cv2
import numpy as np
import time

pag.PAUSE = 0.2

# nox
# button position
left_button = pag.locateOnScreen("button_left.png")
right_button = pag.locateOnScreen("button_right.png")
# icon position
left_icon_pos = {"left": left_button.left + 80, "top": left_button.top - 140, "width": 90, "height": 90}
right_icon_pos = {"left": right_button.left - 100, "top": right_button.top - 140, "width": 90, "height": 90}

def compute_icon_type(img):
    mean = np.mean(img, axis=(0, 1))
    result = None
    if mean[0] > 50 and mean[0] < 55 and mean[1] > 50 and mean[1] < 55\
            and mean[2] > 50 and mean[2] < 55:
        result = "BOMB"
    elif mean[0] > 250 and mean[1] > 85 and mean[1] < 110 and mean[2] > 250:
        result = "SWORD"
    elif mean[0] > 100 and mean[0] < 130 and mean[1] > 150 and mean[1] < 200\
            and mean[2] > 90 and mean[2] < 110:
        result = "POISON"
    elif mean[0] > 210 and mean[0] < 230 and mean[1] > 200 and mean[1] < 225\
            and mean[2] > 120 and mean[2] < 135:
        result = "JEWEL"
    return result

def click(coords):
    pag.click(coords[0],coords[1])    

while True:
    with mss.mss() as sct:
        left_img = np.array(sct.grab(left_icon_pos))[:, :, :3]
        right_img = np.array(sct.grab(right_icon_pos))[:, :, :3]
        # cv2.imshow("left_img", left_img)
        # cv2.imshow("right_img", right_img)
        # cv2.waitKey(0)

        left_icon = compute_icon_type(left_img)
        right_icon = compute_icon_type(right_img)

        if left_icon == 'SWORD' and (right_icon == 'BOMB' or right_icon == 'POISON'):
            print('TAP LEFT!')
            click(pag.center(left_button))
            # n_fails = 0
        elif right_icon == 'SWORD' and (left_icon == 'BOMB' or left_icon == 'POISON'):
            print('TAP RIGHT!')
            click(pag.center(right_button))
            # n_fails = 0
        elif left_icon == 'JEWEL' and right_icon == 'JEWEL':
            print('FEVER!')
            fever = time.time()
            while True:
                click(pag.center(left_button))
                click(pag.center(right_button))
                if fever + 3 > time.time():
                    break
        else:
            print('FAIL')
            # n_fails += 1
            # if n_fails > fail_limit:
            #     print('failed %s times, terminate!' % (fail_limit))
            #     break
