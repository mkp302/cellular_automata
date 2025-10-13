import json
from pathlib import Path


class Config:
    def __init__(self, path):
        self.path = Path(path)
        self.data = {}
        self.load()

    def load(self):
        if not self.path.exists():
            raise FileNotFoundError(f"File not found: {self.path}")
        with open(self.path, "r") as f:
            self.data = json.load(f)

    def get(self, *keys, default=None):
        value = self.data
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return default
        return value if value is not None else default
