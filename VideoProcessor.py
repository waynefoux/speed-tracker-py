import cv2


class VideoProcessor:

    def __init__(self, video_feed):

        # Initialize service
        self.capture = cv2.VideoCapture(video_feed)

        # Create a background subtractor
        # If we detect shadows it will slow down the processing
        self.fgbg = cv2.createBackgroundSubtractorMOG2(history=-1, detectShadows=False)

        # TODO - make comments why you are doing this...
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))


    # Starts the service
    def start(self):
        while():

            # Get a single from from the capture
            ret, frame = self.capture.read()

            foo = self.fgbg.apply(frame)
            fgmask = foo
            cv2.imshow('frame', fgmask)

            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break

            _, image_threshold = cv2.threshold(fgmask, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            image_threshold = cv2.erode(image_threshold, np.ones((11, 11)))
            image_threshold = cv2.GaussianBlur(image_threshold, (5, 5), 0)
            # sorting contours by size
            _, contours, hierarchy = cv2.findContours(image_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            contours = sorted(contours, key=cv2.contourArea)

            # if (len(contours) > 0):
            #    print("Contours " + str(len(contours)))

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

    # Stops the service
    def stop(self):
        self.capture.release()
        cv2.destroyAllWindows()

    def withinWindow(self, valid_contours):
        window_contour = []
        for rect in valid_contours:
            x, y, w, h = rect
            if x > 200 and x < 400:
                window_contour.append(rect)

        return window_contour


        #cv2.rectangle(frame, (x, y), (x-200 + w+200, y-200 + h+200), (255, 255, 0), 2)
        #cv2.putText(frame, 'Moth Detected', (x + w + 10, y + h), 0, 0.3, (255, 255, 0))
        #cv2.imshow("Show", frame)


if __name__ == "__main__":

    videoProcessor = VideoProcessor('http://192.168.0.4:8088/video')
