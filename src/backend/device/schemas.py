from src.common.schema import SchemaBase


class Device(SchemaBase):
    device_id: str
    notification_token: str | None
    device_type: int

class DeviceAddRequest(Device):
    ''' Device Add Request '''