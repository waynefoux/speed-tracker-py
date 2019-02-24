import time

CONVERSION = .681818

class Target:

    def __init__(self, location, pixels_per_foot):
        self.pixels_per_foot = pixels_per_foot
        self.last_location = location
        self.last_time = get_time()
        self.total = 0
        self.count = 0

    # Get the speed of the targeted item.
    def get_speed(self, location):

        # Calculate distance traveled
        distance_traveled = abs(self.last_location - location)
        current_time = get_time()
        time_domain = (current_time - self.last_time) / 1000

        # Set last location to the current location
        self.last_location = location
        self.last_time = current_time

        feet_traveled = float(distance_traveled) / self.pixels_per_foot
        feet_per_sec = float(feet_traveled) / time_domain
        mph = int(round(feet_per_sec * CONVERSION))


        self.total = self.total + mph
        self.count = self.count + 1

        return distance_traveled, time_domain

    def get_average_speed(self):
        if self.count > 0:
            return self.total / self.count

def get_time():

    return time.time() * 1000.00



