from django.db import models

from apps.catalog.models import Track
from apps.core.models import UUIDTimeStampedModel


class MusicLicense(UUIDTimeStampedModel):
    """Contractual license metadata for catalog distribution (not legal advice)."""

    code = models.SlugField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    external_reference = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = "licensing_music_license"
        ordering = ("code",)

    def __str__(self):
        return self.name


class LegalSource(UUIDTimeStampedModel):
    """
    A verified partner or rights-holder system that may supply metadata or files.
    BeatIQ does not scrape or rip third-party UGC platforms.
    """

    class SourceKind(models.TextChoices):
        PARTNER_CATALOG = "partner_catalog", "Partner catalog API"
        RIGHTS_HOLDER_PORTAL = "rights_holder_portal", "Rights-holder portal"
        USER_OWNED_FILE = "user_owned_file", "User-owned upload (creator flow)"
        OTHER_VERIFIED = "other_verified", "Other verified legal source"

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True)
    kind = models.CharField(
        max_length=32,
        choices=SourceKind.choices,
        default=SourceKind.PARTNER_CATALOG,
    )
    base_url = models.URLField(max_length=500, blank=True)
    is_verified_partner = models.BooleanField(default=False, db_index=True)

    class Meta:
        db_table = "licensing_legal_source"

    def __str__(self):
        return self.name


class LicensedTrackSource(UUIDTimeStampedModel):
    """
    Canonical mapping between a Track and a specific legal distribution channel.
    Download eligibility is evaluated ONLY through linked DownloadPermission rows.
    """

    track = models.ForeignKey(
        Track,
        on_delete=models.CASCADE,
        related_name="licensed_sources",
    )
    legal_source = models.ForeignKey(
        LegalSource,
        on_delete=models.PROTECT,
        related_name="licensed_tracks",
    )
    license = models.ForeignKey(
        MusicLicense,
        on_delete=models.PROTECT,
        related_name="licensed_track_sources",
    )
    partner_track_id = models.CharField(max_length=255, blank=True)
    canonical_reference_url = models.URLField(
        max_length=800,
        blank=True,
        help_text="Human-readable reference on partner site (not a rip target).",
    )
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = "licensing_licensed_track_source"
        unique_together = ("track", "legal_source", "partner_track_id")

    def __str__(self):
        return f"{self.track_id} @ {self.legal_source.slug}"


class DownloadPermission(UUIDTimeStampedModel):
    """
    Explicit grant that downloads may be issued for files originating from the
    linked LicensedTrackSource. Without allows_download=True, APIs must refuse.
    """

    licensed_track_source = models.OneToOneField(
        LicensedTrackSource,
        on_delete=models.CASCADE,
        related_name="download_permission",
    )
    allows_download = models.BooleanField(default=False, db_index=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_until = models.DateTimeField(null=True, blank=True)
    max_bitrate_kbps = models.PositiveIntegerField(null=True, blank=True)
    requires_subscription_plan = models.ForeignKey(
        "subscriptions.Plan",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="download_permissions",
        help_text="If set, user must have active subscription at or above this tier.",
    )
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "licensing_download_permission"

    def __str__(self):
        return f"DL perm for {self.licensed_track_source_id}: {self.allows_download}"
