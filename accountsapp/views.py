from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from .models import *
import uuid
import random
from django.core.mail import send_mail
from django.conf import settings

def register(request: HttpRequest):
    error_text = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        
        if email and password and confirm_password and first_name and last_name and phone_number:
            if '@' in email:
                if len(password) >= 8:
                    if password == confirm_password:
                        try:
                            user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
                            MyUser.objects.create(user=user, phone_number=phone_number)
                            
                            # Create a registration code and send an email
                            code = str(random.randint(100000, 999999))
                            RegistrationCode.objects.create(user=user, code=code)
                            send_mail(
                                subject="Підтвердіть свою реєстрацію в інтернет магазині",
                                message=f"Введіть даний код для активації Вашого акаунту: {code}",
                                from_email=settings.EMAIL_HOST_USER,
                                recipient_list=[email]
                            )
                            
                            # Перенаправлення для активації користувача
                            return redirect(f'/accounts/activate/{user.id}/')
                        except IntegrityError:
                            error_text = 'Даний email вже використовується.'
                    else:
                        error_text = 'Паролі не співпадають.'
                else:
                    error_text = 'Пароль повинен бути більше 8 символів.'
            else:
                error_text = 'Введіть вірний email.'
        else:
            error_text = 'Введіть дані у всі обовязкові поля.'
    
    context = {}
    if error_text:
        context['error_text'] = error_text

    return render(request, 'accountsapp/register.html', context)

def activate(request: HttpRequest, user_id: int):
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        user_code = request.POST.get('code')
        if user_code:
            try:
                registration_code = RegistrationCode.objects.get(user=user, code=user_code)
                user.is_active = True
                user.save()
                registration_code.delete()  # Після успішної реєстрації видаляєм код реєстрації
                
                # Входимо після активації
                login(request, user)
                
                # Перенаправляєм на профіль
                return redirect('profile')
            except RegistrationCode.DoesNotExist:
                context = {'error_text': 'Невірний код активації.'}
                return render(request, 'accountsapp/activate.html', context)
    
    return render(request, 'accountsapp/activate.html')
def logout_view(request:HttpRequest):
    logout(request)
    return redirect('product_list')

def auth(request: HttpRequest):
    error_text = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                return redirect('profile')
            else:
                error_text = 'Логін або пароль неправильний'
    context = {}
    if error_text:
        context['error_text'] = error_text
    return render(request, 'accountsapp/auth.html', context)

def profile(request:HttpRequest):
    return render(request, 'accountsapp/profile.html')


def comments(request:HttpRequest):
    session_comment = request.COOKIES.get('session_comment')
    if not session_comment:
        session_comment = uuid.uuid4().hex
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Comment.objects.create(text = text, 
                                   id_anonymous_user = session_comment)
    context = {
        'comments': Comment.objects.all(),
        'session_comment': session_comment
    }
    response = render(request, 'accountsapp/test.html', context)
    response.set_cookie('session_comment', session_comment)
    return response