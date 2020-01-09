import pyautogui as pag
import mss
import cv2
import numpy as np

pag.PAUSE = 0.05

# nox
# icon position
left_icon_pos = {"left": 640, "top": 685, "width": 90, "height": 90}
right_icon_pos = {"left": 840, "top": 685, "width": 90, "height": 90}
# button position
left_button = [570, 830]
right_button = [935, 830]

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
    pag.moveTo(x=coords[0], y=coords[1], duration= 0.0)
    pag.mouseDown()
    pag.mouseUp()

while True:
    # x, y = pag.position()
    # position_str = "X: " + str(x) + "Y: " + str(y)
    # print(position_str)

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
            click(left_button)
            # n_fails = 0
        elif right_icon == 'SWORD' and (left_icon == 'BOMB' or left_icon == 'POISON'):
            print('TAP RIGHT!')
            click(right_button)
            # n_fails = 0
        elif left_icon == 'JEWEL' and right_icon == 'JEWEL':
            print('FEVER!')
            click(left_button)
            click(right_button)
            # n_fails = 0
            # fever = time.time()
        else:
            print('FAIL')
            # n_fails += 1
            # if n_fails > fail_limit:
            #     print('failed %s times, terminate!' % (fail_limit))
            #     break
