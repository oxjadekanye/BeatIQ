"""Vendor-agnostic AI client surface (implement with httpx/requests + retries)."""

from __future__ import annotations

import os
from typing import Any


class AIProviderClient:
    def __init__(self) -> None:
        self.api_key = os.environ.get("AI_PROVIDER_API_KEY", "")
        self.base_url = os.environ.get("AI_PROVIDER_BASE_URL", "").rstrip("/")

    def infer(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError("Wire your AI vendor here.")
