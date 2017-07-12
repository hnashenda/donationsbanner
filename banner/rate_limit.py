from time import time, sleep
from collections import defaultdict
from threading import Lock
import logging
from django.conf import settings


class TokenBucket:
    """
    An implementation of the token bucket algorithm.
    """
    def __init__(self, capacity, rate, min_interval=0):
        self.capacity = capacity
        self.tokens = capacity
        self.rate = rate
        self.min_interval = min_interval
        self.last = time()

        def default_values():
            return {
                "tokens" : self.capacity,
                "last" : self.last,
                "lock" : Lock()
            }

        self.uids = defaultdict(default_values)

    def consume(self, uid, tokens=1):
        with self.uids[uid]["lock"]:
            now = time()
            lapse = now - self.uids[uid]["last"]
            self.uids[uid]["last"] = now
            self.uids[uid]["tokens"] += lapse * self.rate
            
            if self.uids[uid]["tokens"] > self.capacity:
                self.uids[uid]["tokens"] = self.capacity

            if self.uids[uid]["tokens"] == self.capacity:
                first = True
            else:
                first = False

            self.uids[uid]["tokens"] -= tokens

            if self.uids[uid]["tokens"] < self.min_interval:
                sleep(-self.uids[uid]["tokens"] / self.rate)
			#logging.debug("hello hubert")
                #print(uid, -self.uids[uid]["tokens"] / self.rate)
            else:
                if not first:
                    sleep(self.min_interval)
                #print(uid, self.min_interval)
				#logging.debug("hello hubert")


if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor
    
    bucket = TokenBucket(40, 2, .05)
    futs = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        for _ in range(100):
            futs.append( executor.submit(bucket.consume, "foo") )
        for _ in range(50) :
            futs.append( executor.submit(bucket.consume, "bar") )

    [ fut.result() for fut in futs ]