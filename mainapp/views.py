from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from .forms import RegisterForm, LoginForm
from django.core.mail import send_mail





def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # save user manually
            User.objects.create(username=username, password=password)

            messages.success(request, "Account created successfully")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # check user manually
            user = User.objects.filter(username=username, password=password).first()

            if user:
                request.session['user_id'] = user.id  # simple session login
                messages.success(request, "Login successful")
                return redirect('home')
            else:
                messages.error(request, "Invalid credentials")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def home(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user = User.objects.get(id=request.session['user_id'])

    return render(request, 'home.html', {'user': user})


def logout_view(request):
    request.session.flush()
    return redirect('login')

def profile(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user = User.objects.get(id=request.session['user_id'])
    return render(request, 'profile.html', {'user': user})

def settings(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user = User.objects.get(id=request.session['user_id'])

    if request.method == 'POST':
        user.username = request.POST.get('username')

        password = request.POST.get('password')
        if password:
            user.password = password

        user.save()

    return render(request, 'settings.html', {'user': user})

def send_message(request):
    if request.method == "POST":
        send_mail(
            subject="Wellness Alert",
            message="This is a message from Wellness Dashboard.",
            from_email="sahlauk237@gmail.com",
            recipient_list=["sahlauk28@gmail.com"],
            fail_silently=False,
        )
        print(" EMAIL SENT SUCCESSFULLY") 
        messages.success(request, "Message sent successfully!")
    return redirect('home') 

def forgot_password(request):
    if request.method == "POST":
        username = request.POST.get("username")
        new_password = request.POST.get("new_password")

        try:
            user = User.objects.get(username=username)
            user.password = new_password  
            user.save()
            return redirect('login')
        except User.DoesNotExist:
            pass

    return render(request, 'forgot_password.html')