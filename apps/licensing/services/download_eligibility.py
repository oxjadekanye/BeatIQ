"""
Legal download permission evaluation.

BeatIQ must never facilitate platform ripping, DRM bypass, or unauthorized copying.
This module centralizes the *only* allowed path: explicit `DownloadPermission` rows
bound to verified `LicensedTrackSource` records.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Any

from django.utils import timezone

if TYPE_CHECKING:
    from apps.accounts.models import User
    from apps.catalog.models import Track
    from apps.licensing.models import DownloadPermission, LicensedTrackSource


@dataclass(frozen=True)
class DownloadEligibilityResult:
    allowed: bool
    reason_code: str
    detail: str
    licensed_track_source_id: str | None = None
    permission_id: str | None = None


def _now() -> datetime:
    return timezone.now()


def _user_meets_plan_requirement(user: "User", permission: "DownloadPermission") -> bool:
    plan = permission.requires_subscription_plan
    if plan is None:
        return True
    from apps.subscriptions.models import Subscription

    sub = (
        Subscription.objects.filter(user=user, status=Subscription.Status.ACTIVE)
        .select_related("plan")
        .order_by("-current_period_end")
        .first()
    )
    if not sub or not sub.plan:
        return False
    return sub.plan.tier_order >= plan.tier_order


def evaluate_download(
    user: "User",
    licensed_track_source: "LicensedTrackSource",
) -> DownloadEligibilityResult:
    from apps.licensing.models import DownloadPermission

    if not licensed_track_source.is_active:
        return DownloadEligibilityResult(
            False,
            "SOURCE_INACTIVE",
            "Licensed source is inactive.",
            str(licensed_track_source.id),
            None,
        )

    try:
        perm: DownloadPermission = licensed_track_source.download_permission
    except DownloadPermission.DoesNotExist:
        return DownloadEligibilityResult(
            False,
            "NO_DOWNLOAD_PERMISSION",
            "No explicit download permission exists for this legal source mapping.",
            str(licensed_track_source.id),
            None,
        )

    if not perm.allows_download:
        return DownloadEligibilityResult(
            False,
            "DOWNLOADS_DISABLED",
            "Partner license does not grant downloads for this asset.",
            str(licensed_track_source.id),
            str(perm.id),
        )

    now = _now()
    if perm.valid_from and now < perm.valid_from:
        return DownloadEligibilityResult(
            False,
            "PERMISSION_NOT_YET_VALID",
            "Download permission is not yet effective.",
            str(licensed_track_source.id),
            str(perm.id),
        )
    if perm.valid_until and now > perm.valid_until:
        return DownloadEligibilityResult(
            False,
            "PERMISSION_EXPIRED",
            "Download permission has expired.",
            str(licensed_track_source.id),
            str(perm.id),
        )

    if not _user_meets_plan_requirement(user, perm):
        return DownloadEligibilityResult(
            False,
            "SUBSCRIPTION_REQUIRED",
            "Active subscription tier insufficient for this download grant.",
            str(licensed_track_source.id),
            str(perm.id),
        )

    return DownloadEligibilityResult(
        True,
        "OK",
        "Explicit download permission satisfied.",
        str(licensed_track_source.id),
        str(perm.id),
    )


def pick_best_eligible_source(user: "User", track: "Track") -> DownloadEligibilityResult:
    from apps.licensing.models import LicensedTrackSource

    qs = (
        LicensedTrackSource.objects.filter(track=track, is_active=True)
        .select_related(
            "download_permission",
            "download_permission__requires_subscription_plan",
        )
        .order_by("created_at")
    )
    first = None
    for lts in qs:
        if first is None:
            first = lts
        result = evaluate_download(user, lts)
        if result.allowed:
            return result
    if first is None:
        return DownloadEligibilityResult(
            False,
            "NO_LEGAL_SOURCE",
            "Track has no registered legal distribution sources.",
            None,
            None,
        )
    return evaluate_download(user, first)


def summarize_track_download_policy(user: "User", track: "Track") -> dict[str, Any]:
    result = pick_best_eligible_source(user, track)
    return {
        "track_id": str(track.id),
        "download_allowed": result.allowed,
        "reason_code": result.reason_code,
        "detail": result.detail,
        "licensed_track_source_id": result.licensed_track_source_id,
        "download_permission_id": result.permission_id,
    }
