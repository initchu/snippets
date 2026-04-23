from dataclasses import dataclass, field
from typing import List


@dataclass
class Config:
    host: str = "localhost"
    port: int = 8080
    tags: List[str] = field(default_factory=list)
    debug: bool = False

    def endpoint(self) -> str:
        return f"http://{self.host}:{self.port}"

# 2026-04-23 08:00:12
