import datetime

from django.http import JsonResponse
from django.views import View
from anychat.settings import SECRET_KEY
from django.contrib import auth
from google.appengine.api import mail
import jwt
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from utils.jwt_auth import create_token


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(View):
    def post(self, request):
        """ JWT 登录 """
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        result = {
            'status': False
        }
        if user is not None:
            result = {
                'status': True,
                'token': create_token(user)
            }
        return JsonResponse(result)
