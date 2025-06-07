import httpx
from asgiref.sync import sync_to_async
from fastapi import Request
from ip2loc import XdbSearcher
from user_agents import parse
from typing import Optional

from src.common.data_classes import IpInfo, UserAgentInfo
from src.common.log import log
from src.core.settings import settings
from src.core.path_config import path_config
from src.database.redis import redis

class RequestParser:

    def get_request_ip(self, request: Request) -> str:
        """
        Get the IP address of the request with multiple fallbacks and validation
        """
        # Try common proxy headers first
        for header in ['X-Real-IP', 'X-Forwarded-For', 'CF-Connecting-IP']:
            if header in request.headers:
                ips = request.headers[header].split(',')
                if ips:
                    ip = ips[0].strip()
                    if self._is_valid_ip(ip):
                        return ip

        # Fallback to direct connection IP
        if not request.client or not request.client.host:
            return '0.0.0.0'

        # Handle test cases
        if request.client.host == 'testclient':
            return '127.0.0.1'

        return request.client.host if self._is_valid_ip(request.client.host) else '0.0.0.0'

    def _is_valid_ip(self, ip: str) -> bool:
        """
        Basic IP address validation
        """
        if not ip or not isinstance(ip, str):
            return False
        
        # Quick check for common invalid patterns
        if ip.lower() in ['unknown', 'none', 'null', '']:
            return False
            
        # Basic format check (doesn't validate all cases but catches obvious issues)
        parts = ip.split('.')
        if len(parts) == 4:
            try:
                return all(0 <= int(part) <= 255 for part in parts)
            except (ValueError, AttributeError):
                pass
        return False

    async def get_location_online(self, ip: str, user_agent: str) -> Optional[dict]:
        """
        Get IP address location online with proper error handling
        """
        if not self._is_valid_ip(ip) or ip == '0.0.0.0':
            return None

        async with httpx.AsyncClient(timeout=3) as client:
            ip_api_url = f'http://ip-api.com/json/{ip}?lang=zh-CN'
            headers = {'User-Agent': user_agent or 'Mozilla/5.0'}
            try:
                response = await client.get(ip_api_url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('status') == 'success':
                        return data
            except Exception as e:
                log.warning(f'Online IP lookup failed for {ip}: {str(e)}')
            return None

    @sync_to_async
    def get_location_offline(self, ip: str) -> Optional[dict]:
        """
        Get IP address location offline with robust error handling
        """
        if not self._is_valid_ip(ip) or ip == '0.0.0.0':
            return None

        try:
            cb = XdbSearcher.loadContentFromFile(dbfile=path_config.ip2region__xdb)
            searcher = XdbSearcher(contentBuff=cb)
            data = searcher.search(ip)
            searcher.close()
            
            if not data:
                return None
                
            data = data.split('|')
            return {
                'country': data[0] if data[0] != '0' else None,
                'regionName': data[2] if data[2] != '0' else None,
                'city': data[3] if data[3] != '0' else None,
            }
        except Exception as e:
            log.warning(f'Offline IP lookup failed for {ip}: {str(e)}')
            return None

    async def parse_ip_info(self, request: Request) -> IpInfo:
        """
        Parse IP information with caching and fallback logic
        """
        ip = self.get_request_ip(request)
        
        # Check cache first
        cache_key = f'{settings.IP_LOCATION_REDIS_PREFIX}:{ip}'
        cached = await redis.get(cache_key) if ip != '0.0.0.0' else None
        
        if cached:
            try:
                country, region, city = cached.split('|')
                return IpInfo(ip=ip, country=country, region=region, city=city)
            except Exception:
                pass  # Fall through to fresh lookup

        # Get fresh location data
        location_info = None
        if settings.IP_LOCATION_PARSE == 'online':
            location_info = await self.get_location_online(ip, request.headers.get('User-Agent'))
        elif settings.IP_LOCATION_PARSE == 'offline':
            location_info = await self.get_location_offline(ip)

        # Process and cache results
        country = region = city = None
        if location_info:
            country = location_info.get('country')
            region = location_info.get('regionName', location_info.get('region'))
            city = location_info.get('city')
            
            if ip != '0.0.0.0':
                await redis.set(
                    cache_key,
                    f'{country or ""}|{region or ""}|{city or ""}',
                    ex=settings.IP_LOCATION_EXPIRE_SECONDS,
                )

        return IpInfo(ip=ip, country=country, region=region, city=city)

    def parse_user_agent_info(self, request: Request) -> UserAgentInfo:
        """
        Parse user agent information with fallback values
        """
        user_agent = request.headers.get('User-Agent', '')
        try:
            _user_agent = parse(user_agent)
            return UserAgentInfo(
                user_agent=user_agent,
                device=_user_agent.get_device() or 'Unknown',
                os=_user_agent.get_os() or 'Unknown',
                browser=_user_agent.get_browser() or 'Unknown'
            )
        except Exception as e:
            log.warning(f'User agent parsing failed: {str(e)}')
            return UserAgentInfo(
                user_agent=user_agent,
                device='Unknown',
                os='Unknown',
                browser='Unknown'
            )

request_parser: RequestParser = RequestParser()