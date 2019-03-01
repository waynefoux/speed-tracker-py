import cv2
import target
import logging
import statistics

# This needs to move to the main class...
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.DEBUG)

DEFAULT_VIDEO_SOURCE = 'http://192.168.0.4:8088/video'      # A streaming location or locaton of file
VIDEO_ENABLED = True
ESCAPE_KEY = 27                                             # The numerical value of ESC
MINIMUM_AREA = 2000                                         # The smallest area in pixels we expect a vehicle to be
FRAME_NAME = "SpeedCam"                                     # Main frame name
DISTANCE_IN_FEET = 50


class VideoProcessor:

    def __init__(self, video_feed, video_enabled):

        # Logging
        self.logger = logging.getLogger(__name__)

        # Initialize service
        self.capture = cv2.VideoCapture(video_feed)
        self.video_enabled = video_enabled
        self.statistics = statistics.Statistics()

        cv2.namedWindow(FRAME_NAME, flags=cv2.WINDOW_NORMAL)

        cv2.setMouseCallback(FRAME_NAME, self.click_event)

        self.target = None
        self.left = None
        self.right = None
        self.pixel_to_feet = None

        ret, frame = self.capture.read()

        self.height, self.width, _ = frame.shape

        #calibrator.calibrate(frame)

        cv2.imshow(FRAME_NAME, frame)
        cv2.waitKey(0)
        # if not self.video_enabled:
        #     cv2.destroyWindow(FRAME_NAME)
        #     cv2.waitKey()

        pixel_distance = abs(self.left - self.right)
        self.pixels_per_foot = pixel_distance / DISTANCE_IN_FEET

    # Starts the service
    def start(self):
        self.logger.info("Beginning video processing.")

        # Create background subtractor
        background_subtractor = cv2.createBackgroundSubtractorMOG2(history=30, detectShadows=False)

        first_frame = None

        while True:

            # Check if we need to quit
            key = cv2.waitKey(30) & 0xff
            if key == ESCAPE_KEY:
                break

            # Capture the frame
            ret, frame = self.capture.read()

            # We need to do stuff to figure out about the images
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 11), 0)

            # I think I did this to bootstrap the subtractors
            if first_frame is None:
                first_frame = gray
                continue

            foreground_frame = background_subtractor.apply(gray)

            # Do stuff to frame
            _, image_threshold = cv2.threshold(foreground_frame, 0, 255, cv2.THRESH_BINARY)
            image_threshold = cv2.dilate(image_threshold, None, iterations=3)

            # Find contours and sort by size
            contours, hierarchy = cv2.findContours(image_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            contours = sorted(contours, key=cv2.contourArea)

            num_of_cars = 0

            # For each contour we are going to look to see if it meets the requirement of of what a vehicle might be.
            for contour in contours:

                # Get the bonding rectangle of the contour
                rect = cv2.boundingRect(contour)
                x, y, w, h = rect

                # If a contour's area is bigger than the minimum area we defined we likely have a car to track.
                area = w * h
                if area > MINIMUM_AREA:

                    num_of_cars = num_of_cars + 1
                    self.mark_object(frame, rect)

            # We will only measure if we see one car
            if num_of_cars == 1 and (x > self.left and (x + w) < self.right):
                center_of_target = x + (w/2)
                if self.target is None:
                    self.target = target.Target(center_of_target, self.pixels_per_foot)
                else:
                    _ = self.target.get_speed_in_mph(center_of_target)
            else:
                # If no cars or more than one are found but one has just passed, get its average speed and clear it.
                if self.target is not None:
                    # TODO : Need to figure this error handling out.
                    try:
                        average_speed = self.target.get_average_speed_in_mph()
                        self.logger.info("Vehicle speed: %sMPH", average_speed)
                        self.statistics.add_target(average_speed,
                                                   self.target.get_direction_of_travel(),
                                                   None,
                                                   None)
                    except Exception:
                        self.logger.error("Error")
                    finally:
                        self.target = None

            if self.video_enabled:
                cv2.imshow(FRAME_NAME, frame)

                # Can be used for image debugging
                #cv2.imshow('"Forground Frame', image_threshold)

    # Mark the object on the frame
    def mark_object(self, frame, rect):
        x, y, h, w = rect
        area = w * h
        cv2.rectangle(frame, (x, y), (x - 200 + w + 200, y - 200 + h + 200), (255, 255, 0), 2)
        cv2.putText(frame, str(area), (x + w + 10, y + h), 0, 0.3, (255, 255, 0))

    # Stops the service
    def stop(self):
        self.capture.release()
        cv2.destroyAllWindows()

    # Need a better way to do this???
    def click_event(self, event, x, y, flags, param):
        global run
        global frame

        if event == cv2.EVENT_LBUTTONDOWN:
            self.left = x
        elif event == cv2.EVENT_LBUTTONUP:
            self.right = x

    # Helps in debugging
    def screen_data_refresh(self, frame):

        # Draw checkpoints
        cv2.line(frame, (self.left, self.height - 10), (self.left, 10), (0, 0, 0))
        cv2.line(frame, (self.right, self.height - 10), (self.right, 10), (0, 0, 0))


if __name__ == "__main__":

    # Instantiate Video Processor
    videoProcessor = VideoProcessor(DEFAULT_VIDEO_SOURCE, VIDEO_ENABLED)

    # Start processing
    videoProcessor.start()
