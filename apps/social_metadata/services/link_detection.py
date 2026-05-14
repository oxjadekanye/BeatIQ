"""Strict allowlisted URL parsing — extend with partner oEmbed only."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from apps.social_metadata.models import SocialLinkMetadata

if TYPE_CHECKING:
    from apps.accounts.models import User

logger = logging.getLogger("beatiq.social")


def resolve_share_url(url: str, user: User | None = None) -> SocialLinkMetadata:
    parsed = urlparse(url)
    normalized = parsed.geturl()
    platform = SocialLinkMetadata.Platform.UNKNOWN
    if parsed.hostname and "partner" in parsed.hostname:
        platform = SocialLinkMetadata.Platform.PARTNER

    meta = SocialLinkMetadata.objects.create(
        submitted_by=user,
        raw_url=url[:800],
        normalized_url=normalized[:800],
        platform=platform,
        raw_metadata={
            "host": parsed.hostname,
            "note": "Do not add UGC ripping parsers here; use verified partner APIs only.",
        },
    )
    logger.info("social_link_stub id=%s", meta.id)
    return meta
