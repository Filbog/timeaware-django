from django.shortcuts import render, redirect
from django.contrib.auth import login

# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy

# for email registration confirmation
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .models import CustomUser


def signup(request):

    if request.user.is_authenticated:
        return redirect("learning_logs:index")

    if request.method != "POST":
        form = CustomUserCreationForm()
    else:
        form = CustomUserCreationForm(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # generate email confirmation link
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # message content
            current_site = get_current_site(request)
            mail_subject = "Activate your account."
            message = render_to_string(
                "registration/activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": uid,
                    "token": token,
                },
            )
            # send email
            send_mail(mail_subject, message, "mywebsite@mywebsite.com", [user.email])
            return render(request, "registration/signup_succesful.html")
    context = {"form": form}
    return render(request, "registration/signup.html", context)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, "registration/email_confirmation_successful.html")
        else:
            return render(request, "registration/activation_link_invalid.html")
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        return render(request, "registration/activation_link_invalid.html")
