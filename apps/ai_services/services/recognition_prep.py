from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.ai_services.models import AIRecognitionPrepJob

logger = logging.getLogger("beatiq.ai")


def enqueue_recognition_prep(job: AIRecognitionPrepJob) -> str:
    from apps.ai_services.tasks import recognition_prep_task

    recognition_prep_task.delay(str(job.id))
    logger.info("recognition_prep_enqueued id=%s", job.id)
    return str(job.id)
