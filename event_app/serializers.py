from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.hashers import make_password

from events.settings import EMAIL_HOST_USER
from .models import Profile, Event, Response, User, Reply
from .utils import get_mail_subject, get_mail_context


class UserSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='users-detail', read_only=True)

    def create(self, validated_data):
        user = self.Meta.model(**validated_data)
        user.password = make_password(user.password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.set_password(validated_data.pop("password", ""))
        return super().update(instance, validated_data)

    class Meta:
        model = User
        queryset = model.objects.all()
        fields = ("id", "url", "username", "email", "password", "is_superuser", "is_event_creator")


class ProfileSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='profiles-detail', read_only=True)
    events = SerializerMethodField()

    def get_events(self, obj):
        return obj.user.is_event_creator

    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ['slug', 'user']


class EventSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='events-detail', read_only=True)
    participants = SerializerMethodField()

    def get_participants(self, obj):

        if obj.event_type == "to response":
            serializer = ResponseSerializer(obj.responses, many=True, context=self.context)
        else:
            serializer = ResponseSerializer(obj.participates, many=True, context=self.context)
        return serializer.data

    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ['host']


class ResponseSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='responses-detail', read_only=True)

    def create(self, validated_data):
        response = self.Meta.model(**validated_data)
        if response.event_title.event_type == "to participate":
            raise ValidationError("This event is reply only")

        send_mail(get_mail_subject(response.event_title.host.username, response.event_title),
                  get_mail_context(response.event_title, response.username, "отклик"),
                  EMAIL_HOST_USER, (response.event_title.host.email,)
                  )

        response.save()
        return response

    def update(self, instance, validated_data):
        if validated_data['event_title'].event_type == "to participate":
            raise ValidationError("This event is reply only")

        return super().update(instance, validated_data)

    class Meta:
        model = Response
        fields = "__all__"
        read_only_fields = ['username']


class ReplySerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='replies-detail', read_only=True)

    def create(self, validated_data):
        reply = self.Meta.model(**validated_data)
        if reply.event_title.event_type == "to response":
            raise ValidationError("This event is response only")

        send_mail(get_mail_subject(reply.event_title.host.username, reply.event_title),
                  get_mail_context(reply.event_title, reply.username, "заявку"),
                  EMAIL_HOST_USER, (reply.event_title.host.email,)
                  )

        reply.save()
        return reply

    def update(self, instance, validated_data):
        if validated_data['event_title'].event_type == "to response":
            raise ValidationError("This event is response only")

        return super().update(instance, validated_data)

    class Meta:
        model = Reply
        fields = "__all__"
        read_only_fields = ['username']
