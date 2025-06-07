import sys
from redis.asyncio import Redis
from redis.exceptions import AuthenticationError, TimeoutError

from src.core.settings import settings
from src.common.log import log

class RedisCli(Redis):
    def __init__(self) -> None:
        redis_client = Redis.from_url(
            settings.REDIS_URL,
            socket_timeout=settings.REDIS_TIMEOUT,
            socket_connect_timeout=5,
            socket_keepalive=True,
            health_check_interval=30,
            decode_responses=True,
            retry_on_timeout=True,
            max_connections=20,
        )
        
        super().__init__(connection_pool=redis_client.connection_pool)

    async def open(self) -> None:
        try:
            await self.ping()
        except TimeoutError:
            log.error('❌ Redis database connection timeout')
            sys.exit()
        except AuthenticationError:
            log.error('❌ Redis database connection authentication failure')
            sys.exit()
        except Exception as e:
            log.error('❌ Redis database connection exception {}', e)
            sys.exit()

    async def delete_prefix(self, prefix: str, exclude: str | list[str] | None = None) -> None:
        keys = []
        async for key in self.scan_iter(match=f'{prefix}*'):
            if isinstance(exclude, str):
                if key != exclude:
                    keys.append(key)
            elif isinstance(exclude, list):
                if key not in exclude:
                    keys.append(key)
            else:
                keys.append(key)
        if keys:
            await self.delete(*keys)

redis: RedisCli = RedisCli()