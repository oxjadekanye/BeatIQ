"""Shared DRF helpers (e.g. drf-spectacular schema generation)."""


def is_schema_generation(view) -> bool:
    """True when drf-spectacular introspects the view with a fake request."""
    return getattr(view, "swagger_fake_view", False)
