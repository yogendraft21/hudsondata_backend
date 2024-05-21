from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException

class RateLimiter:
    def __init__(self, limit: int, window: int):
        self.limit = limit
        self.window = window
        self.tokens = limit
        self.last_refill = datetime.utcnow()

    def refill_tokens(self):
        now = datetime.utcnow()
        time_passed = (now - self.last_refill).total_seconds()
        refill_amount = int(time_passed / self.window) * self.limit
        self.tokens = min(self.limit, self.tokens + refill_amount)
        self.last_refill = now

    def acquire(self):
        self.refill_tokens()
        if self.tokens <= 0:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        self.tokens -= 1

limiter = RateLimiter(limit=3, window=60)

def rate_limit():
    limiter.acquire()
