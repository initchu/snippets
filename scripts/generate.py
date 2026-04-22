"""
DevPulse Actions – commit generator
====================================
Reads COMMIT_COUNT from env (default 1), generates that many realistic
commits with coherent file content and Conventional Commit messages.

Each commit writes a file whose content matches its extension, then
commits immediately so multiple green squares appear when COMMIT_COUNT > 1.
"""

from __future__ import annotations

import os
import random
import string
import subprocess
from datetime import datetime
from pathlib import Path

# ── Repo root (one level up from scripts/) ──────────────────────────────────
REPO_ROOT = Path(__file__).parent.parent

# ── Directory → allowed extensions ──────────────────────────────────────────
DIR_EXTENSIONS: dict[str, list[str]] = {
    "src":      [".py"],
    "docs":     [".md", ".txt"],
    "tests":    [".py", ".txt"],
    "examples": [".py", ".json", ".yaml"],
    "scripts":  [".py"],
}

# ── Commit message templates (Conventional Commits) ─────────────────────────
COMMIT_TEMPLATES: dict[str, list[str]] = {
    "feat": [
        "feat: add retry mechanism with configurable back-off",
        "feat: introduce chunked iterator utility",
        "feat: add HMAC-SHA256 payload signing helper",
        "feat: support JSON load/save with UTF-8 encoding",
        "feat: add timed decorator for performance logging",
        "feat: implement Config dataclass with endpoint helper",
        "feat: add health-check endpoint to API",
        "feat: support pagination on events listing",
        "feat: add structured logging with context fields",
        "feat: implement token bucket rate limiter",
        "feat: add async task queue with priority support",
        "feat: introduce circuit breaker for external calls",
    ],
    "fix": [
        "fix: resolve N+1 query in user listing endpoint",
        "fix: handle encoding errors when reading existing files",
        "fix: prevent race condition in concurrent log writes",
        "fix: correct HMAC comparison to use constant-time check",
        "fix: avoid division by zero in metrics aggregation",
        "fix: correct off-by-one in pagination offset calculation",
        "fix: sanitise user input before passing to shell command",
    ],
    "refactor": [
        "refactor: extract content generation into per-extension methods",
        "refactor: simplify token masking logic in run_cmd",
        "refactor: replace magic strings with named constants",
        "refactor: consolidate file-walk logic into helper method",
        "refactor: move config validation to dedicated module",
    ],
    "docs": [
        "docs: add architecture overview document",
        "docs: update contributing guide with code style section",
        "docs: add API reference for jobs endpoint",
        "docs: document retry utility in module docstring",
        "docs: update changelog for unreleased changes",
        "docs: add sequence diagram for auth flow",
    ],
    "chore": [
        "chore: upgrade PyYAML to 6.0.1",
        "chore: add CI pipeline configuration",
        "chore: update application config schema",
        "chore: clean up unused imports",
        "chore: pin dependency versions in requirements.txt",
        "chore: remove deprecated helper functions",
    ],
    "test": [
        "test: add unit tests for HMAC signing helper",
        "test: cover edge cases in chunked iterator",
        "test: add integration test for auth flow",
        "test: fix flaky assertion in test_worker",
        "test: increase coverage for config validation",
    ],
    "perf": [
        "perf: add DB index to reduce query time by 85%",
        "perf: cache frequently read config values in Redis",
        "perf: reduce memory footprint under high concurrency",
        "perf: batch database writes to reduce round-trips",
    ],
}

# feat and fix appear most often, like real projects
CATEGORY_WEIGHTS = [5, 4, 2, 2, 2, 1, 1]


# ── Content generators ───────────────────────────────────────────────────────

def _py() -> str:
    return random.choice([
        '''\
import logging

logger = logging.getLogger(__name__)


def retry(func, max_attempts: int = 3, delay: float = 1.0):
    """Retry a callable up to *max_attempts* times with a fixed *delay*."""
    import time
    for attempt in range(1, max_attempts + 1):
        try:
            return func()
        except Exception as exc:
            logger.warning("Attempt %d/%d failed: %s", attempt, max_attempts, exc)
            if attempt == max_attempts:
                raise
            time.sleep(delay)
''',
        '''\
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
''',
        '''\
import hashlib
import hmac


def sign_payload(payload: bytes, secret: str) -> str:
    """Return HMAC-SHA256 hex digest for *payload* using *secret*."""
    key = secret.encode()
    return hmac.new(key, payload, hashlib.sha256).hexdigest()


def verify_signature(payload: bytes, secret: str, signature: str) -> bool:
    expected = sign_payload(payload, secret)
    return hmac.compare_digest(expected, signature)
''',
        '''\
from pathlib import Path
import json


def load_json(path) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save_json(data: dict, path, indent: int = 2) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=indent)
''',
        '''\
import time
from functools import wraps


def timed(func):
    """Decorator that logs execution time of *func*."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} finished in {elapsed:.4f}s")
        return result
    return wrapper
''',
        '''\
import threading


class TokenBucket:
    """Thread-safe token bucket rate limiter."""

    def __init__(self, rate: float, capacity: float) -> None:
        self._rate = rate
        self._capacity = capacity
        self._tokens = capacity
        self._lock = threading.Lock()
        self._last = __import__("time").monotonic()

    def consume(self, tokens: float = 1.0) -> bool:
        with self._lock:
            now = __import__("time").monotonic()
            self._tokens = min(
                self._capacity,
                self._tokens + (now - self._last) * self._rate,
            )
            self._last = now
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False
''',
        '''\
import sqlite3
from contextlib import contextmanager


@contextmanager
def get_connection(db_path):
    """Yield a SQLite connection with WAL mode and foreign keys enabled."""
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
''',
    ])


def _md() -> str:
    return random.choice([
        '''\
# Architecture Overview

## Components

- **API Gateway** – routes incoming requests to the appropriate service
- **Core Service** – handles business logic and data processing
- **Storage Layer** – persists data using a relational database

## Data Flow

```
Client → API Gateway → Core Service → Storage Layer
```
''',
        '''\
# Contributing Guide

1. Fork the repository and clone your fork.
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Make your changes and add tests where appropriate.
4. Run the test suite: `pytest`
5. Open a pull request against `main`.

## Code Style

Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code.
''',
        '''\
# Changelog

## [Unreleased]

### Added
- Configurable retry logic for network requests
- Token bucket rate limiter for external API calls

### Fixed
- Race condition when multiple workers write to the same log file
- Off-by-one error in pagination offset calculation
''',
        '''\
# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | ✅        |
| < 1.0   | ❌        |

## Reporting a Vulnerability

Please email security@example.com with a description and steps to reproduce.
We aim to respond within 48 hours.
''',
    ])


def _txt() -> str:
    return random.choice([
        '''\
Performance profiling notes
============================
- Identified N+1 query in user listing; fixed with select_related()
- Reduced average response time from 320 ms to 45 ms after adding DB index
- Memory usage stable at ~180 MB under 500 concurrent connections
''',
        '''\
TODO list
=========
- [ ] Add pagination to /api/v1/events endpoint
- [ ] Write integration tests for the auth flow
- [x] Upgrade PyYAML to 6.0.1
- [x] Add health-check endpoint
''',
        '''\
Code review checklist
======================
[ ] Logic is correct and handles edge cases
[ ] No sensitive data in code or comments
[ ] Functions are small and single-responsibility
[ ] Error paths are handled and logged
[ ] New code has corresponding tests
''',
    ])


def _yaml() -> str:
    return random.choice([
        '''\
app:
  name: devpulse
  version: "1.0.0"
  log_level: info

server:
  host: 0.0.0.0
  port: 8080
  workers: 4
  timeout: 30
''',
        '''\
metrics:
  enabled: true
  port: 9090
  path: /metrics

alerts:
  - name: high_error_rate
    condition: error_rate > 0.05
    severity: critical
  - name: slow_response
    condition: p99_latency_ms > 500
    severity: warning
''',
    ])


def _json() -> str:
    return random.choice([
        '''\
{
  "name": "devpulse",
  "version": "1.0.0",
  "description": "Automated GitHub activity generator",
  "dependencies": {
    "pyyaml": "6.0.1",
    "schedule": "1.2.0"
  }
}
''',
        '''\
{
  "openapi": "3.0.3",
  "info": { "title": "DevPulse API", "version": "1.0.0" },
  "paths": {
    "/health": {
      "get": {
        "summary": "Health check",
        "responses": { "200": { "description": "OK" } }
      }
    }
  }
}
''',
    ])


CONTENT_GENERATORS = {
    ".py":   _py,
    ".md":   _md,
    ".txt":  _txt,
    ".yaml": _yaml,
    ".yml":  _yaml,
    ".json": _json,
}


# ── Helpers ──────────────────────────────────────────────────────────────────

def pick_commit_message() -> str:
    categories = list(COMMIT_TEMPLATES.keys())
    category = random.choices(categories, weights=CATEGORY_WEIGHTS, k=1)[0]
    return random.choice(COMMIT_TEMPLATES[category])


def pick_file_path() -> Path:
    existing: list[Path] = []
    for d in DIR_EXTENSIONS:
        dir_path = REPO_ROOT / d
        if dir_path.exists():
            for f in dir_path.iterdir():
                if f.is_file() and not f.name.startswith("."):
                    existing.append(f)

    if existing and random.random() < 0.55:
        return random.choice(existing)

    directory = random.choice(list(DIR_EXTENSIONS.keys()))
    ext = random.choice(DIR_EXTENSIONS[directory])
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return REPO_ROOT / directory / f"{directory}_{suffix}{ext}"


def write_file(path: Path) -> None:
    ext = path.suffix.lower()
    content = CONTENT_GENERATORS.get(ext, _txt)()

    # Always append a timestamp so git detects a change every run
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stamp = {
        ".py":   f"\n# updated: {ts}\n",
        ".md":   f"\n<!-- updated: {ts} -->\n",
        ".txt":  f"\n# updated: {ts}\n",
        ".yaml": f"\n# updated: {ts}\n",
        ".yml":  f"\n# updated: {ts}\n",
        ".json": f'\n  "updated": "{ts}"\n',
    }.get(ext, f"\n# updated: {ts}\n")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content + stamp, encoding="utf-8")


def git(*args: str) -> None:
    subprocess.run(["git", *args], cwd=REPO_ROOT, check=True)


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    commit_count = int(os.environ.get("COMMIT_COUNT", "1"))
    commit_count = max(1, min(commit_count, 5))

    print(f"[{datetime.now()}] Generating {commit_count} commit(s)")

    for i in range(commit_count):
        file_path = pick_file_path()
        write_file(file_path)

        rel = file_path.relative_to(REPO_ROOT)
        git("add", str(rel))

        msg = pick_commit_message()
        git("commit", "-m", msg)

        print(f"[{datetime.now()}] [{i+1}/{commit_count}] {msg}  →  {rel}")


if __name__ == "__main__":
    main()
