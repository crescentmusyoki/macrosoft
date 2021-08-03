from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction, IntegrityError, DatabaseError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from calculator.forms import LoginForm, RegisterForm, ProfileForm, CustomPasswordChangeForm, CalculationForm
import numexpr as ne

# login view
from calculator.models import Calculation


class LoginView(View):
    template_name = 'calculator/login.html'
    context = {
        'active_login': True,
        'page_title': 'Log in'
    }

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('home-view'))
        self.context['form'] = LoginForm()
        return render(request, self.template_name, self.context)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('home-view'))
        form = LoginForm(request.POST)
        self.context['form'] = form

        if form.is_valid():
            authed_user = authenticate(request,
                                       username=form.cleaned_data['username'],
                                       password=form.cleaned_data['password'])
            if authed_user is not None:
                login(request, authed_user)
                messages.success(request, 'Successfully logged in')
                return redirect(reverse('home-view'))
            else:
                messages.warning(request, 'Invalid login details')
                return render(request, self.template_name, self.context)
        else:
            messages.warning(request, form.errors)
            return render(request, self.template_name, self.context)


# register view
class RegisterView(View):
    template_name = 'calculator/register.html'
    context = {
        'active_register': True,
        'page_title': 'Register'
    }

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('home-view'))
        self.context['form'] = RegisterForm()
        return render(request, self.template_name, self.context)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('home-view'))
        form = RegisterForm(request.POST)
        self.context['form'] = form

        if form.is_valid():
            try:
                with transaction.atomic():
                    auth_user = form.save()
                    auth_user.first_name = form.cleaned_data['first_name']
                    auth_user.last_name = form.cleaned_data['last_name']
                    auth_user.set_password(form.cleaned_data['password2'])
                    auth_user.save()

                    # auth user for now
                    authed_user = authenticate(request,
                                               username=form.cleaned_data['username'],
                                               password=form.cleaned_data['password2'])
                    if authed_user is not None:
                        login(request, authed_user)

                    messages.success(request, 'Successfully registered')
                    return redirect(reverse('home-view'))

            except IntegrityError as e:
                messages.warning(request, e.__str__())
            except DatabaseError as e:
                messages.warning(request, e.__str__())

            return redirect(reverse('register-view'))
        else:
            messages.warning(request, form.errors)
            return render(request, self.template_name, self.context)


# log out
def logout_view(request):
    logout(request)
    return redirect(reverse('login-view'))


# Home view
class HomeView(LoginRequiredMixin, View):
    template_name = 'calculator/home.html'
    context = {
        'active_home': True,
        'page_title': 'Home'
    }

    def get(self, request, *args, **kwargs):
        self.context['form'] = CalculationForm()
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = CalculationForm(request.POST)
        self.context['form'] = form

        if form.is_valid():
            question_answer = None
            question = form.cleaned_data['calculation_expression']
            question_save = Calculation()
            question_save.calculation_expression = question
            question_save.user = request.user
            question_save.save()
            try:

                question_answer = eval(question)

                question_save.calculation_answer = question_answer
                question_save.save()
            except (SyntaxError, NameError, TypeError, ZeroDivisionError) as e:
                messages.warning(request, e.__str__())

                question_save.calculation_answer = e.__str__()
                question_save.save()
            self.context['question_answer'] = question_answer
        else:
            messages.warning(request, form.errors)
        return render(request, self.template_name, self.context)


# Profile view
class ProfileView(LoginRequiredMixin, View):
    template_name = 'calculator/profile.html'
    context = {
        'active_profile': True,
        'page_title': 'Profile'
    }

    def get(self, request):
        self.context['form'] = ProfileForm(instance=request.user)
        self.context['password_form'] = CustomPasswordChangeForm(request.user)
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user)
        self.context['form'] = form

        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated')
            return redirect(reverse('profile-view'))
        else:
            messages.warning(request, form.errors)
            return render(request, self.template_name, self.context)


# change password view
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.error(request, form.errors)

    return redirect(reverse('profile-view'))


# History view
class HistoryView(LoginRequiredMixin, View):
    template_name = 'calculator/history.html'
    context = {
        'active_history': True,
        'page_title': 'History'
    }

    def get(self, request):
        self.context['calculations'] = Calculation.objects.filter(user=request.user)
        return render(request, self.template_name, self.context)
