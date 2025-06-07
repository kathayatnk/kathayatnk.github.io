from pathlib import Path


class PathConfig:
    def __init__(self):
        self.base_path = Path(__file__).resolve().parent.parent
        self.log_dir = self.base_path / 'log'
        self.static_dir = self.base_path / 'static'
        self.alembic_version_dir = self.base_path / 'alembic' / 'versions'
        self.service_account_key_path = self.base_path / 'swipewise-69429-firebase-adminsdk-fbsvc-8019cb9aaa.json'
        self.ip2region__xdb = self.static_dir / 'ip2region.xdb'


path_config: PathConfig = PathConfig()