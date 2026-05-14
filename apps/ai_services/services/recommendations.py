"""
Placeholder integration with an external AI vendor.

Enqueue paths delegate to Celery (`apps.ai_services.tasks`). With
`CELERY_TASK_ALWAYS_EAGER=True` (development), work runs inline.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.playlists.models import AIPlaylistRecommendation

logger = logging.getLogger("beatiq.ai")


def enqueue_playlist_recommendation_job(recommendation: AIPlaylistRecommendation) -> str:
    from apps.ai_services.tasks import playlist_recommendation_task

    playlist_recommendation_task.delay(str(recommendation.id))
    logger.info("playlist_recommendation_enqueued id=%s", recommendation.id)
    return str(recommendation.id)
