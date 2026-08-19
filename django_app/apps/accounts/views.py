from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View
from .models import LoginAttempt, AdminUser

def client_ip(request): return request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR','')).split(',')[0].strip()
class AdminLoginView(View):
    template_name = 'admin_panel/admin-login.html'
    def get(self, request): return render(request, self.template_name)
    def post(self, request):
        ip, email = client_ip(request), request.POST.get('email','').strip().lower()
        key = f'admin-login:{ip}:{email}'
        failures = cache.get(key, 0)
        if failures >= 5:
            LoginAttempt.objects.create(email=email, ip_address=ip, successful=False)
            messages.error(request, 'Too many failed attempts. Try again in 15 minutes.')
            return render(request, self.template_name, {'locked': True})
        user = authenticate(request, email=email, password=request.POST.get('password',''))
        LoginAttempt.objects.create(email=email, ip_address=ip, successful=bool(user))
        if user is None:
            failures = cache.incr(key) if cache.get(key) is not None else 1
            cache.set(key, failures, 900)
            messages.error(request, 'Invalid credentials.')
            return render(request, self.template_name, {'warning': failures >= 3})
        cache.delete(key); login(request, user); request.session.set_expiry(28800)
        return redirect('core:dashboard')
class AdminLogoutView(View):
    def post(self, request): logout(request); return redirect('accounts:login')

class StudentRegisterView(View):
    template_name = 'student/student_register.html'
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.role == 'student':
                return redirect('public_blog:my_blogs')
            return redirect('core:dashboard')
        return render(request, self.template_name)
        
    def post(self, request):
        email = request.POST.get('email', '').strip().lower()
        name = request.POST.get('name', '').strip()
        password = request.POST.get('password', '')
        
        if not email or not name or not password:
            messages.error(request, 'All fields are required.')
            return render(request, self.template_name)
            
        if AdminUser.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, self.template_name)
            
        user = AdminUser.objects.create_user(email=email, password=password, first_name=name, role='student')
        login(request, user)
        messages.success(request, 'Registration successful! Welcome to your portal.')
        return redirect('public_blog:my_blogs')

class StudentLoginView(View):
    template_name = 'student/student_login.html'
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.role == 'student':
                return redirect('public_blog:my_blogs')
            return redirect('core:dashboard')
        return render(request, self.template_name)
        
    def post(self, request):
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        
        if not email or not password:
            messages.error(request, 'Email and password are required.')
            return render(request, self.template_name)
            
        user = authenticate(request, email=email, password=password)
        if user is None:
            messages.error(request, 'Invalid credentials.')
            return render(request, self.template_name)
            
        if not user.is_active:
            messages.error(request, 'Your account is disabled.')
            return render(request, self.template_name)
            
        if user.role != 'student':
            messages.error(request, 'Access denied. This portal is only for students.')
            return render(request, self.template_name)
            
        login(request, user)
        request.session.set_expiry(28800)
        messages.success(request, f'Welcome back, {user.first_name}!')
        return redirect('public_blog:my_blogs')

class StudentLogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('student_accounts:login')
