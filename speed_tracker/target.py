import time
import logging

CONVERSION_FACTOR = .681818             # The multiplier to convert feet/sec to miles/hour
MINIMUM_DATA_POINTS = 4                 # The lowest number of data points we will except for a valid speed

# The object we are tracking
class Target:

    def __init__(self, location, pixels_per_foot):

        # Logging
        self.logger = logging.getLogger(__name__)

        self.pixels_per_foot = pixels_per_foot      # The number of pixels that make up a foot
        self.last_location = location               # The last pixel location of the target
        self.direction_of_travel = None             # Direction of travel
        self.last_time_stamp = get_time_stamp()     # The last time stamp we saw the target
        self.list_of_mph = []                       # List of mph collected

    # Get the speed of the targeted item.
    def get_speed_in_mph(self, location):

        # Get current time
        current_time_stamp = get_time_stamp()

        # Calculate distance traveled
        delta = self.last_location - location
        distance_traveled = abs(delta)
        time_domain = (current_time_stamp - self.last_time_stamp) / 1000

        #Calculate direction
        if delta < 0:
            self.direction_of_travel = "<"
        else:
            self.direction_of_travel = ">"

        # Calculate miles/hour
        feet_traveled = float(distance_traveled) / self.pixels_per_foot
        feet_per_sec = float(feet_traveled) / time_domain
        mph = round(feet_per_sec * CONVERSION_FACTOR)

        # Update data on target
        self.list_of_mph.append(mph)

        # Set last location to the current location
        self.last_location = location
        self.last_time_stamp = current_time_stamp

        return mph

    def get_average_speed_in_mph(self):
        if len(self.list_of_mph) > 0:
            self.logger.debug("Data points collected: %s", len(self.list_of_mph))

            sum_of_mph = 0
            for mph in self.list_of_mph:
                sum_of_mph = sum_of_mph + mph

            # Consider returning standard deviation...
            if len(self.list_of_mph) < 4:
                raise Exception('Not enough data points')

            return round(sum_of_mph / len(self.list_of_mph))

    def get_direction_of_travel(self):
        return self.direction_of_travel

    def get_direction_of_travel(self):
        return self.direction_of_travel

def get_time_stamp():
    return time.time() * 1000.00



