from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from .models import Profile, Event, Response, User, Reply
from .permissions import IsAuthorOrReadOnly, IsEventMaker
from .serializers import ProfileSerializer, EventSerializer, ResponseSerializer, UserSerializer, ReplySerializer


class UserViewSet(ModelViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all().select_related("user")
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthorOrReadOnly,)


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsEventMaker,)

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)


class ResponseViewSet(ModelViewSet):
    queryset = Response.objects.all().select_related("event_title")
    serializer_class = ResponseSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(username=self.request.user)


class ReplyViewSet(ModelViewSet):
    queryset = Reply.objects.all().select_related("event_title")
    serializer_class = ReplySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(username=self.request.user)
