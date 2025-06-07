from typing import Any
from starlette.responses import JSONResponse
from msgspec import json

class MsgSpecJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return json.encode(content)