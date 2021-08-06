from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy
from django.utils.text import slugify


class User(AbstractUser):
    email = models.EmailField(('email address'), unique=True)

    is_event_creator = models.BooleanField(
        ('event creator status'),
        default=False,
        help_text=(
            'Designates whether this user should be treated as events maker. '
        ),
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, verbose_name="Url", unique=True)
    bio = models.TextField(blank=True, verbose_name='About yourself')
    city = models.CharField(max_length=60, blank=True)
    profile_picture = models.ImageField(upload_to="useravatars/%Y/%m/%d/", blank=True, verbose_name="profile picture")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ["user"]

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance, slug=slugify(instance.username))

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def get_absolute_url(self):
        return reverse_lazy("profile", kwargs={"slug": self.slug, })


class Event(models.Model):
    TYPE_CHOICES = (
        ('to participate', 'to participate'),
        ('to response', 'to response'),
    )
    title = models.CharField(max_length=100)
    event_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='to response')
    content = models.TextField(blank=True, verbose_name='About event', )
    city = models.CharField(max_length=60, blank=True)
    host = models.ForeignKey(User, verbose_name="host", on_delete=models.CASCADE, related_name='hosts')
    date = models.DateTimeField(verbose_name="Date")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation date", )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse_lazy("event", kwargs={"pk": self.pk, })


class Response(models.Model):
    event_title = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='responses')
    username = models.ForeignKey(User, verbose_name="username", on_delete=models.CASCADE, related_name='user_responses')
    content = models.TextField(blank=True, verbose_name='Response')
    date = models.DateTimeField(auto_now_add=True, verbose_name="Reply date", )
    files = models.FileField(upload_to="responses/%Y/%m/%d/", blank=True, verbose_name="Response file", )

    def __str__(self):
        return f"{self.event_title} + {self.username}"

    class Meta:
        verbose_name = "Response"
        verbose_name_plural = "Responses"
        ordering = ["-date"]


class Reply(models.Model):
    event_title = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participates')
    username = models.ForeignKey(User, verbose_name="username", on_delete=models.CASCADE, related_name='user_replies')
    content = models.TextField(blank=True, verbose_name='Reply')
    date = models.DateTimeField(auto_now_add=True, verbose_name="Reply date", )

    def __str__(self):
        return f"{self.event_title} + {self.username}"

    class Meta:
        verbose_name = "Reply"
        verbose_name_plural = "Replies"
        ordering = ["-date"]
