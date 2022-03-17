from django.conf import Settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils import timezone

from backend.users.models import User, TwoFactorAuth

def activate(request):
    user = User.objects.all().filter(username=request.POST.get("user", ""))
    if not user:
        return HttpResponse('Unable to find user name!')
    
    authqueryset = TwoFactorAuth.objects.all()

    fetch_auth = authqueryset.filter(user_id=user.get().id, auth_token=request.POST.get("auth_token", ""))
    
    if not fetch_auth:
        return HttpResponse('Activation token is expired!')

    user.update(is_active=True)

    return HttpResponse('Account activated successfully!')