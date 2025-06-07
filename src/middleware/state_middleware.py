from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.utils.request_parser import request_parser


class StateMiddleware(BaseHTTPMiddleware):
    """Request state middleware for parsing and setting additional request information"""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        ip_info = await request_parser.parse_ip_info(request)
        ua_info = request_parser.parse_user_agent_info(request)

        # Set additional request information
        request.state.ip = ip_info.ip
        request.state.country = ip_info.country
        request.state.region = ip_info.region
        request.state.city = ip_info.city
        request.state.user_agent = ua_info.user_agent
        request.state.os = ua_info.os
        request.state.browser = ua_info.browser
        request.state.device = ua_info.device

        response = await call_next(request)

        return response