from threading import Lock

class CityLocks:
    def __init__(self):
        # Initialize an empty dictionary to store locks for each city
        self.city_locks = {}
        # Create a lock to protect the city_locks dictionary
        self.write_lock = Lock()

    def get_lock(self, city):
        if city not in self.city_locks:
            # If the lock for this city doesn't exist, create it
            with self.write_lock:
                self.city_locks[city] = Lock()
                return self.city_locks[city]
        
        else:
            # Otherwise, return the existing lock for this city
            return self.city_locks[city]
