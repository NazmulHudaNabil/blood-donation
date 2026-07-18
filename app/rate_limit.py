from slowapi import Limiter
from slowapi.util import get_remote_address

# Shared limiter instance — imported by both app/main.py (to register it on the
# app) and individual route modules (to decorate specific endpoints), which
# avoids a main.py <-> routes circular import.
limiter = Limiter(key_func=get_remote_address)
