from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.ai_services.models import AIMoodDiscoverySession

logger = logging.getLogger("beatiq.ai")


def enqueue_mood_discovery(session: AIMoodDiscoverySession) -> str:
    from apps.ai_services.tasks import mood_discovery_task

    mood_discovery_task.delay(str(session.id))
    logger.info("mood_discovery_enqueued id=%s", session.id)
    return str(session.id)
