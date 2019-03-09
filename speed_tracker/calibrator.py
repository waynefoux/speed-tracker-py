import cv2

FRAME_NAME = "calibration"

# This class will take over calibration that was happening in videoProcessor
class Calibrator:

def calibrate(capture):
    ret, frame = capture.read()

    cv2.namedWindow(FRAME_NAME, flags=cv2.WINDOW_NORMAL)

    cv2.setMouseCallback(FRAME_NAME, click_event)

    cv2.imshow(FRAME_NAME, frame)
    cv2.waitKey(0)
    cv2.destroyWindow(FRAME_NAME)
    cv2.waitKey()


# Need a better way to do this???
def click_event(event, x, y, flags, param):
    global run
    global frame

    if event == cv2.EVENT_LBUTTONDOWN:
        left = x
    elif event == cv2.EVENT_LBUTTONUP:
        right = x


if __name__ == "__main__":
    capture = cv2.VideoCapture('http://192.168.0.4:8088/video')

    calibrate(capture)
