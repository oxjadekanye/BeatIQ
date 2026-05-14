"""Load minimal catalog rows for local API testing (idempotent)."""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.catalog.models import Album, Artist, Genre, Track


class Command(BaseCommand):
    help = "Create sample genres, artists, albums, and tracks (safe to re-run)."

    @transaction.atomic
    def handle(self, *args, **options):
        genres_data = [
            ("Electronic", "electronic"),
            ("Hip Hop", "hip-hop"),
            ("Jazz", "jazz"),
        ]
        genres = {}
        for name, slug in genres_data:
            g, created = Genre.objects.get_or_create(slug=slug, defaults={"name": name})
            genres[slug] = g
            if created:
                self.stdout.write(f"  + genre {name}")

        artists_data = [
            ("Nova Pulse", "nova-pulse", "Synth-forward electronic duo."),
            ("The Midnight Keys", "the-midnight-keys", "Instrumental jazz trio."),
        ]
        artists = {}
        for name, slug, bio in artists_data:
            a, created = Artist.objects.get_or_create(slug=slug, defaults={"name": name, "bio": bio})
            artists[slug] = a
            if created:
                self.stdout.write(f"  + artist {name}")

        albums_data = [
            ("nova-pulse", "Horizons EP", "horizons-ep", "2024-03-15"),
            ("the-midnight-keys", "Blue Room Sessions", "blue-room-sessions", "2023-11-01"),
        ]
        albums = {}
        for artist_slug, title, slug, rd in albums_data:
            artist = artists[artist_slug]
            alb, created = Album.objects.get_or_create(
                artist=artist,
                slug=slug,
                defaults={"title": title, "release_date": rd},
            )
            albums[f"{artist_slug}:{slug}"] = alb
            if created:
                self.stdout.write(f"  + album {title}")

        tracks_data = [
            (
                "nova-pulse",
                "horizons-ep",
                "Signal Rise",
                "signal-rise",
                214000,
                ["electronic"],
            ),
            (
                "nova-pulse",
                "horizons-ep",
                "Glassline",
                "glassline",
                198500,
                ["electronic"],
            ),
            (
                "the-midnight-keys",
                "blue-room-sessions",
                "Slow Bloom",
                "slow-bloom",
                312000,
                ["jazz"],
            ),
            (
                "the-midnight-keys",
                "blue-room-sessions",
                "Paper Moon Redux",
                "paper-moon-redux",
                245000,
                ["jazz", "hip-hop"],
            ),
        ]
        for artist_slug, album_slug, title, track_slug, duration_ms, genre_slugs in tracks_data:
            artist = artists[artist_slug]
            album = albums[f"{artist_slug}:{album_slug}"]
            t, created = Track.objects.get_or_create(
                primary_artist=artist,
                slug=track_slug,
                defaults={
                    "title": title,
                    "album": album,
                    "duration_ms": duration_ms,
                },
            )
            t.genres.set([genres[gs] for gs in genre_slugs])
            if created:
                self.stdout.write(f"  + track {title}")

        self.stdout.write(self.style.SUCCESS("Catalog seed complete."))
