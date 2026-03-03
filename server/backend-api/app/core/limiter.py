import os
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address

logger = logging.getLogger(__name__)


def _get_rate_limit_key_func():
    """
    Get the appropriate key function for rate limiting.
    
    Uses X-Forwarded-For header if available (for reverse proxy setups),
    otherwise falls back to remote address.
    """
    def key_func(request):
        # Try to get the real IP from X-Forwarded-For header (for reverse proxy)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # Take the first IP (original client)
            return forwarded_for.split(",")[0].strip()
        return get_remote_address(request)
    
    return key_func


# Get Redis URL from environment
REDIS_URL = os.getenv("REDIS_URL", "")

# Configure limiter with dynamic key function
limiter = Limiter(key_func=_get_rate_limit_key_func())

# Configure Redis storage if available
if REDIS_URL:
    # Set Redis as the storage backend
    limiter.storage_uri = REDIS_URL
    logger.info("Rate limiter configured with Redis backend")
else:
    logger.info(
        "REDIS_URL not configured. Using in-memory rate limiting. "
        "Note: In-memory rate limiting does not work with multiple workers."
    )
