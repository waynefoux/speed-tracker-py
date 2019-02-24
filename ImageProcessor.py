import cv2

class ImageProcessor:

    def __init__(self):
        # Do something

def process_contours(contours):

    valid_contours = []
    for c in contours:
        rect = cv2.boundingRect(c)
        x, y, w, h = rect
        if w > 50 and y < 400 and y > 225:
            valid_contours.append(rect)

    if (len(valid_contours) > 0):
        print("Valid " + str(len(valid_contours)))

    for valid_contour in valid_contours:
        valid_contour
    windowed_contours = self.withinWindow(valid_contours)

    if len(windowed_contours) > 0 and clear:
        clear = False
        count = count + 1
        print(count)
    else:
        clear = True
