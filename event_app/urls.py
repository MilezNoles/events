from rest_framework.routers import DefaultRouter

from .views import ProfileViewSet, EventViewSet, ResponseViewSet, UserViewSet, ReplyViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("profiles", ProfileViewSet, basename="profiles")
router.register("events", EventViewSet, basename="events")
router.register("responses", ResponseViewSet, basename="responses")
router.register("replies", ReplyViewSet, basename="replies")
urlpatterns = router.urls
