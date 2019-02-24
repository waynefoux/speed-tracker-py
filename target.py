import time
import logging

CONVERSION_FACTOR = .681818             # The multiplier to convert feet/sec to miles/hour

# The object we are tracking
class Target:

    def __init__(self, location, pixels_per_foot):

        # Logging
        self.logger = logging.getLogger(__name__)

        self.pixels_per_foot = pixels_per_foot      # The number of pixels that make up a foot
        self.last_location = location               # The last pixel location of the target
        self.last_time_stamp = get_time_stamp()     # The last time stamp we saw the target
        self.sum_of_mph = 0                         # The sum of all the miles/hour seen of this target
        self.count = 0                              # The number of times we saw the target

    # Get the speed of the targeted item.
    def get_speed_in_mph(self, location):

        # Get current time
        current_time_stamp = get_time_stamp()

        # Calculate distance traveled
        distance_traveled = abs(self.last_location - location)
        time_domain = (current_time_stamp - self.last_time_stamp) / 1000

        # Calculate miles/hour
        feet_traveled = float(distance_traveled) / self.pixels_per_foot
        feet_per_sec = float(feet_traveled) / time_domain
        mph = round(feet_per_sec * CONVERSION_FACTOR)

        # Update data on target
        self.sum_of_mph = self.sum_of_mph + mph
        self.count = self.count + 1

        # Set last location to the current location
        self.last_location = location
        self.last_time_stamp = current_time_stamp

        return mph

    def get_average_speed_in_mph(self):
        if self.count > 0:
            return round(self.sum_of_mph / self.count)


def get_time_stamp():
    return time.time() * 1000.00



