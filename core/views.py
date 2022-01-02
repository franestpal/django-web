from django.shortcuts import render 

import stripe
from django.conf import settings
from django.shortcuts import render
from django.views.generic import ListView
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import SuccessURLAllowedHostsMixin, LoginView
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from .forms import CheckoutForm, CouponForm, RefundForm
from .models import *
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm)
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from .forms import UserCreationFormWithEmail
from django import forms
# Create your views here.
import random
import string
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
from .forms import UserCreationFormWithEmail, ProfileForm, EmailForm
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django import forms

from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import (
    url_has_allowed_host_and_scheme, urlsafe_base64_decode,
)
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
import json
from django.http import HttpResponse,HttpResponseForbidden
from django_redis import get_redis_connection
import base64

                                               






# Create your views here.

def home(request):
    return render(request, "core/home.html")

def about(request):
    return render(request, "core/about.html")

def store(request):
    return render(request, "core/store.html")

def CompraOnline(request):
    return render(request, "core/compra_online.html")


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))



# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationFormWithEmail
    template_name = 'core/registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('login') + '?register'   

    def get_form(self, form_class=None):
        form = super(SignUpView, self).get_form()
        # Modificar en tiempo real
        form.fields['username'].widget = forms.TextInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Nombre de usuario'})
        form.fields['email'].widget = forms.EmailInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Dirección email'})
        form.fields['password1'].widget = forms.PasswordInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Contraseña'})
        form.fields['password2'].widget = forms.PasswordInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Repite la contraseña'})
        return form


@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    form_class = ProfileForm
    success_url = reverse_lazy('profile')
    template_name = 'profiles/profile.html'

    def get_object(self):
        # recuperar el objeto que se va editar
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

@method_decorator(login_required, name='dispatch')
class EmailUpdate(UpdateView):
    form_class = EmailForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_email_form.html'

    def get_object(self):
        # recuperar el objeto que se va editar
        return self.request.user

    def get_form(self, form_class=None):
        form = super(EmailUpdate, self).get_form()
        # Modificar en tiempo real
        form.fields['email'].widget = forms.EmailInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Email'})
        return form

from django.contrib.auth.views import LoginView    

class LoginView(SuccessURLAllowedHostsMixin, FormView):
    """
    Display the login form and handle the login action.
    """
    form_class = AuthenticationForm
    authentication_form = None
    template_name = 'core/registration/login.html'






