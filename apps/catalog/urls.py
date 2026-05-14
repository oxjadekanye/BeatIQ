from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AlbumViewSet, ArtistViewSet, GenreViewSet, TrackViewSet

router = DefaultRouter()
router.register("genres", GenreViewSet, basename="catalog-genres")
router.register("artists", ArtistViewSet, basename="catalog-artists")
router.register("albums", AlbumViewSet, basename="catalog-albums")
router.register("tracks", TrackViewSet, basename="catalog-tracks")

urlpatterns = [
    path("", include(router.urls)),
]
