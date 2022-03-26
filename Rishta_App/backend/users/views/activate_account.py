from django.conf import Settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils import timezone

from backend.users.models import User, TwoFactorAuth

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        Users = get_user_model()
        user = Users.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    authqueryset = TwoFactorAuth.objects.all()
    fetch_auth = authqueryset.filter(user_id=user.id, auth_token=token)
    
    if not fetch_auth:
        return HttpResponse('Activation token is expired!')

    user.is_active = True
    user.save()

    return HttpResponse('Account activated successfully!')