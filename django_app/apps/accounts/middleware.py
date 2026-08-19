from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils import timezone
class AutoLogoutMiddleware:
    def __init__(self, get_response): self.get_response = get_response
    def __call__(self, request):
        now = timezone.now().timestamp()
        if request.user.is_authenticated:
            last = request.session.get('last_activity')
            if last and now - last > settings.SESSION_COOKIE_AGE:
                logout(request); return redirect('accounts:login')
            request.session['last_activity'] = now
        return self.get_response(request)
