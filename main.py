import pyautogui
from pynput.mouse import Listener
from pynput.keyboard import Controller
import time



anomaly_coords = (835, 1253)   # Top-left corner (x1, y1)
anomaly_coords2 = (1350, 1283) # Bottom-right corner (x2, y2)
reroll = (1769, 1370)
evolve = (1769, 1270)


# Move the mouse to position (500, 500)
time.sleep(3)
pyautogui.moveTo(anomaly_coords)
time.sleep(1)
pyautogui.moveTo(anomaly_coords2)
time.sleep(1)
pyautogui.moveTo(reroll)
time.sleep(1)
pyautogui.moveTo(evolve)
