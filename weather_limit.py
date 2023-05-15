from datetime import datetime, timedelta

class RequestLimiter:
    def __init__(self, max_requests: int, time_period: int) -> None:
        self.max_requests = max_requests
        self.time_period = time_period
        self.request_info = {}

    # define a function to check if the IP address has exceeded the request limit
    def check_request_limit(self, ip_address: str) -> bool:
        try:
            if ip_address in self.request_info:

                # check if the request count has exceeded the limit
                if self.request_info[ip_address]['count'] >= self.max_requests:
                    last_request_time = self.request_info[ip_address]['last_request_time']
                    time_elapsed = datetime.now() - last_request_time

                    # check if enough time has passed since the last request
                    if time_elapsed < timedelta(minutes=self.time_period):
                        return True
                    else:
                        # reset the request count and last request time
                        self.request_info[ip_address]['count'] = 1
                        self.request_info[ip_address]['last_request_time'] = datetime.now()

                else:
                    # increment the request count for the IP address
                    self.request_info[ip_address]['count'] += 1

            else:
                # create a new entry for the IP address
                self.request_info[ip_address] = {
                    'count': 1,
                    'last_request_time': datetime.now()
                }

            # return False if the request limit has not been exceeded
            return False

        except Exception as e:
            # handle any unexpected errors
            print(f"Error checking request limit: {str(e)}")
            return False

    # define a function to increment the request count for the IP address
    def increment_request_count(self, ip_address: str) -> None:
        try:
            if ip_address in self.request_info:
                self.request_info[ip_address]['count'] += 1
            else:
                self.request_info[ip_address] = {
                    'count': 1,
                    'last_request_time': datetime.now()
                }
        except Exception as e:
            print(f"Error incrementing request count: {str(e)}")
