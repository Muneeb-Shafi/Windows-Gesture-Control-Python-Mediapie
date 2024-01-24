import mediapipe as mp
import cv2
import sys
import io
import pyautogui
import datetime
import ctypes

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode


video = cv2.VideoCapture(0)
paused_frames = 0

def action_trigger(captured_output):
    global paused_frames
    if "Thumb_Up" in captured_output:
        pyautogui.press('volumeup')  # Simulate the volume up keyboard shortcut
        paused_frames += 5
    elif "Thumb_Down" in captured_output:
        pyautogui.press('volumedown')  # Simulate the volume up keyboard shortcut
        paused_frames += 5
    elif "Open_Palm" in captured_output:
        pyautogui.hotkey('win', 'shift', 'm')  # Simulate Win+Shift+M key combination to maximize all windows
        paused_frames += 10
    elif "Closed_Fist" in captured_output:
        pyautogui.hotkey('win', 'm')  # Simulate Win+M key combination to minimize all windows
        paused_frames += 10
    elif "ILoveYou" in captured_output:
        pyautogui.hotkey('win', 'printscreen')  # Simulate Win+PrtScn key combination
        paused_frames += 10
    elif "IHateYou" in captured_output:
        pyautogui.hotkey('win', 'printscreen')  # Simulate Win+PrtScn key combination
        paused_frames += 10
    elif "Victory" in captured_output:
        pyautogui.hotkey('alt', 'f4')  # Simulate Win+M key combination to minimize all windows
        paused_frames += 10
    elif "Pointing_Up" in captured_output:
        pyautogui.hotkey('alt', 'tab')  # Simulate Win+M key combination to minimize all windows
        paused_frames += 10
    else:
        print("Not Detected")

# Create a image segmenter instance with the live stream mode:
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    # cv2.imshow('Show', output_image.numpy_view())
    # imright = output_image.numpy_view()
    result_str = " "
    result_str = result.gestures

    output_string = io.StringIO()
    sys.stdout = output_string
    print(result_str)
    captured_output = output_string.getvalue()
    sys.stdout = sys.__stdout__

    action_trigger(captured_output)

    #print("Captured Output:", captured_output)
    #print(type(captured_output))  # Output: <class 'int'>
    #print(result.gestures)
    # cv2.imwrite('somefile.jpg', imright)


options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='model.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

timestamp = 0
with GestureRecognizer.create_from_options(options) as recognizer:
  # The recognizer is initialized. Use it here.
    while video.isOpened(): 
        # Capture frame-by-frame
        ret, frame = video.read()

        if not ret:
            print("Ignoring empty frame")
            print("Ignore the fork too")
            break

        timestamp += 1

        if paused_frames > 0:
            paused_frames -= 1
        else:
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            recognizer.recognize_async(mp_image, timestamp)


        #mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        # Send live image data to perform gesture recognition
        # The results are accessible via the `result_callback` provided in
        # the `GestureRecognizerOptions` object.
        # The gesture recognizer must be created with the live stream mode.
        #recognizer.recognize_async(mp_image, timestamp)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF


        # If the user pressed the Esc key, stop the loop
        if key == 27:
            break

video.release()
cv2.destroyAllWindows()