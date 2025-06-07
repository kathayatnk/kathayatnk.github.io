
from math import ceil
from fastapi import Request, Response

from src.common.exception import errors


async def http_limit_callback(request: Request, response: Response, expire: int) -> None:  
    expires = ceil(expire / 1000)
    raise errors.HTTPError(code=429, msg='Request rate limit exceeded, please try again later', headers={'Retry-After': str(expires)})
