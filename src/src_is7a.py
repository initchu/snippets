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

# 2026-08-03 04:31:13
