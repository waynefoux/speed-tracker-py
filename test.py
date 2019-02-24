import cv2
import target
import logging


VIDEO_SOURCE = 'http://192.168.0.4:8088/video'      # A streaming location or locaton of file
ESCAPE_KEY = 27                                     # The numerical value of ESC
CONVERSION = .681818

# Logging
logger = logging.getLogger(__name__)
logger.info("foo")


class VideoProcessor:

    def __init__(self, video_feed):

        # Initialize service
        self.capture = cv2.VideoCapture(video_feed)

        # Create background subtractor
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2(history=30, detectShadows=False)

        cv2.namedWindow('Frame', flags=cv2.WINDOW_NORMAL)

        cv2.setMouseCallback('Frame', self.click_event)

        self.target = None
        self.left = None
        self.right = None
        self.pixel_to_feet = None

        ret, frame = self.capture.read()

        self.height, self.width, _ = frame.shape



        cv2.imshow('Frame', frame)

        cv2.waitKey(0)

        print(str(abs(self.left - self.right)))

        pixel_distance = abs(self.left - self.right)

        self.pixels_per_foot = pixel_distance / 50

    # Starts the service
    def start(self):

        first_frame = None

        while True:

            # Check if we need to quit
            key = cv2.waitKey(30) & 0xff
            if key == ESCAPE_KEY:
                break

            # Capture the frame
            ret,frame = self.capture.read()

            # We need to do stuff to figure out about the images
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 11), 0)
            #gray = cv2.erode(gray, None, iterations=10)

            # I think I did this to bootstrap the subtractors
            if first_frame is None:
                first_frame = gray
                continue

            #frame_delta = cv2.absdiff(first_frame, gray)

            foreground_frame = self.background_subtractor.apply(gray)

            # Do stuff to frame
            _, image_threshold = cv2.threshold(foreground_frame, 0, 255, cv2.THRESH_BINARY)

            #cv2.erode(image_threshold, None, iterations=1)

            image_threshold = cv2.dilate(image_threshold, None, iterations=3)

            # sorting contours by size
            contours, hierarchy = cv2.findContours(image_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            contours = sorted(contours, key=cv2.contourArea)

            num_of_cars = 0

            for contour in contours:
                rect = cv2.boundingRect(contour)
                x, y, w, h = rect

                area = w * h
                if area > 2000:
                    num_of_cars = num_of_cars + 1

                    cv2.rectangle(frame, (x, y), (x - 200 + w + 200, y - 200 + h + 200), (255, 255, 0), 2)
                    cv2.putText(frame, str(area), (x + w + 10, y + h), 0, 0.3, (255, 255, 0))

            if num_of_cars > 0:
                cv2.putText(frame, str(num_of_cars), (10, 10), 0, 0.3, (255, 255, 0))


            if num_of_cars == 1 and (x > self.left and (x + w) < self.right):
                center_of_target = x + (w/2)
                if self.target is None:
                    self.target = target.Target(center_of_target, self.pixels_per_foot)
                else:
                    _, _ = self.target.get_speed(center_of_target)
            else:
                if self.target is not None:
                    print(str(self.target.get_average_speed()))
                    self.target = None



            cv2.imshow('Frame', frame)
            #cv2.imshow('"Forground Frame', image_threshold)

    # Stops the service
    def stop(self):
        self.capture.release()
        cv2.destroyAllWindows()

    def click_event(self, event, x, y, flags, param):
        global run
        global frame

        if event == cv2.EVENT_LBUTTONDOWN:
            self.left = x
        elif event == cv2.EVENT_LBUTTONUP:
            self.right = x


if __name__ == "__main__":

    # Instantiate Video Processor
    videoProcessor = VideoProcessor(VIDEO_SOURCE)

    # Start processing
    videoProcessor.start()
