from django.contrib.auth import login, logout, get_user_model
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from event_app.forms import ReplyForm, ResponseForm, UserRegister, UserLogin, ProfileForm, EventForm
from event_app.models import Profile, Event
from event_app.utils import get_mail_subject, get_mail_context
from events.settings import EMAIL_HOST_USER

User = get_user_model()
from_email = EMAIL_HOST_USER


def register(request):
    if request.method == "POST":
        form = UserRegister(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            slug = user.profile.slug
            return redirect("profile", slug)

    else:
        form = UserRegister()

    context = {
        "form": form,
    }
    return render(request, "event_front/register.html", context)


def user_login(request):
    if request.method == "POST":
        form = UserLogin(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")

    else:
        form = UserLogin()

    context = {
        "form": form,
    }
    return render(request, "event_front/login.html", context)


def user_logout(request):
    logout(request)
    return redirect("login")


def user_delete(request):
    user = request.user
    if request.method == "POST":
        qs = User.objects.get(pk=user.pk)
        qs.delete()
    return redirect("home")


@transaction.atomic
def profile(request, slug):
    template_name = 'event_front/profile.html'
    profile = get_object_or_404(Profile.objects.select_related("user"), slug=slug)
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect("profile", slug=slug)
    else:
        profile_form = ProfileForm(instance=profile)

    events = Event.objects.filter(host=profile.user).prefetch_related('responses').prefetch_related('participates')

    context = {'profile': profile,
               'form': profile_form,
               "events": events
               }

    return render(request, template_name, context)


class Home(ListView):
    model = Event
    queryset = Event.objects.all().select_related("host")
    template_name = "event_front/index.html"
    paginate_by = 4


def event(request, pk):
    template_name = 'event_front/event_detail.html'
    event = get_object_or_404(Event.objects.select_related("host"), pk=pk)
    new_reply = None
    if event.event_type == "to participate":

        if request.method == 'POST':
            reply_form = ReplyForm(data=request.POST)

            if reply_form.is_valid():
                reply_form.instance.username = request.user
                new_reply = reply_form.save(commit=False)
                new_reply.event_title = event
                send_mail(get_mail_subject(event.host.username, event.title),
                          get_mail_context(event, request.user, "заявку"),
                          EMAIL_HOST_USER, (event.host.email,)
                          )
                new_reply.save()

        else:
            reply_form = ReplyForm()

    else:

        if request.method == 'POST':
            reply_form = ResponseForm(request.POST, request.FILES)

            if reply_form.is_valid():
                reply_form.instance.username = request.user
                new_reply = reply_form.save(commit=False)
                new_reply.event_title = event

                send_mail(get_mail_subject(event.host.username, event.title),
                          get_mail_context(event, request.user, "отклик"),
                          EMAIL_HOST_USER, (event.host.email,)
                          )
                new_reply.save()

        else:
            reply_form = ResponseForm()

    context = {'object': event,
               'form': reply_form,
               "new_reply": new_reply,
               }

    return render(request, template_name, context)


def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)

        if form.is_valid():
            form.instance.host = request.user
            event = form.save()
            pk = event.pk

            return redirect("event", pk)


    else:
        form = EventForm()

    context = {
        "form": form,
    }
    return render(request, "event_front/event_create.html", context)
