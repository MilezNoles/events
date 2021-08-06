from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Event, Response, Reply
from django.utils.safestring import mark_safe


@admin.register(User)
class UserAdminModified(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_event_creator', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),

    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_event_creator')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'is_event_creator')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "slug", "get_photo",)
    list_display_links = ("user",)
    search_fields = ("user",)
    list_filter = ("user",)

    readonly_fields = ("user", "slug", "get_photo")
    fields = ("user", "slug", "bio", "city", "profile_picture", "get_photo")

    def get_photo(self, obj):
        if obj.profile_picture:
            return mark_safe(f"<img src='{obj.profile_picture.url}' width='50'>")
        else:
            return " - "

    get_photo.short_description = "Profile picture"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'host', 'date', 'created_at')
    list_filter = ('title', 'host', 'date')
    search_fields = ('title', 'host', 'date')


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_title', 'username', 'date')
    list_filter = ('event_title', 'username', 'date')
    search_fields = ('event_title', 'username', 'date')


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_title', 'username', 'date')
    list_filter = ('event_title', 'username', 'date')
    search_fields = ('event_title', 'username', 'date')
