# Import required packages
import time

import pyautogui
import pytesseract
import cv2
import numpy as np
from pynput import keyboard



rolling = True

# Selected anomalies
anomalies = ["ultimate hero"]
reroll_coords = (1769, 1370)
evolve_coords = (1769, 1270)

# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def reroll():
    pyautogui.moveTo(reroll_coords)
    pyautogui.mouseDown()  # Simulate mouse button press
    pyautogui.mouseUp()
    time.sleep(0.2)
    print("Rerolled.")

def evolve():
    pyautogui.moveTo(evolve_coords)
    pyautogui.mouseDown()  # Simulate mouse button press
    pyautogui.mouseUp()

# Function to preprocess the image for OCR
def preprocess_image(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform OTSU thresholding
    _, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # Define the dilation kernel (can adjust size for better result)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))

    # Apply dilation to highlight text contours
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    return gray, thresh1, dilation

# Function to capture screenshot from screen
def capture_and_extract_text(top_left, bottom_right):
    # Calculate the rectangle dimensions
    left = top_left[0]
    top = top_left[1]
    width = bottom_right[0] - top_left[0]
    height = bottom_right[1] - top_left[1]

    # Capture the screenshot from the region defined by top-left and bottom-right coordinates
    screenshot = pyautogui.screenshot(region=(left, top, width, height))

    # Convert screenshot to OpenCV format
    open_cv_image = np.array(screenshot)
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

    # Preprocess the captured image (grayscale, thresholding, dilation)
    gray, _, dilation = preprocess_image(open_cv_image)

    # Find contours in the dilation image
    contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # List to store text and coordinates
    cnt_list = []

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Cropping the text block for OCR
        cropped = gray[y:y + h, x:x + w]

        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)

        # Add the text and its coordinates to the list
        cnt_list.append([x, y, text])

    # Sort the list by y-coordinate (top to bottom order)
    sorted_list = sorted(cnt_list, key=lambda x: x[1])

    # Print the extracted text
    full_text = ""
    for _, _, text in sorted_list:
        if text.strip():  # Avoid printing empty results

            full_text += text
    print("rolled anomaly: ", full_text)

    anomaly_match = False
    global anomalies
    for a in anomalies:
        if  a in full_text.lower():
            anomaly_match = True
            break

    if anomaly_match:
        evolve()
        global rolling
        rolling = False
        print("Evolved with ", full_text)
    else:
        reroll()


# Define the coordinates for top-left and bottom-right corners
anomaly_coords = (835, 1253)   # Top-left corner (x1, y1)
anomaly_coords2 = (1350, 1283) # Bottom-right corner (x2, y2)

# Function to listen for the Insert key press
def on_press(key):
    global rolling
    try:
        if key == keyboard.Key.insert:
            while rolling:
                capture_and_extract_text(anomaly_coords, anomaly_coords2)

        if key == keyboard.Key.home:
            rolling = False

    except AttributeError:
        pass

# Start the keyboard listener
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
