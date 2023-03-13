from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from utils.jwt_auth import parse_payload


class JwtAuthorizationMiddleware(MiddlewareMixin):
    """
    用户需要通过请求头的方式来进行传输token，例如：
    Authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NzM1NTU1NzksInVzZXJuYW1lIjoid3VwZWlxaSIsInVzZXJfaWQiOjF9.xj-7qSts6Yg5Ui55-aUOHJS4KSaeLq5weXMui2IIEJU
    """

    def process_request(self, request):

        # 如果是登录页面，则通过
        if request.path_info == '/user/login':
            return

        # 非登录页面需要校验token
        authorization = request.META.get('HTTP_AUTHORIZATION', '')
        auth = authorization.split()
        # 验证头信息的token信息是否合法
        if not auth:
            return JsonResponse({'error': '未获取到Authorization请求头', 'status': False})
        if auth[0].lower() != 'bearer':
            return JsonResponse({'error': 'Authorization请求头中认证方式错误', 'status': False})
        if len(auth) == 1:
            return JsonResponse({'error': "非法Authorization请求头", 'status': False})
        elif len(auth) > 2:
            return JsonResponse({'error': "非法Authorization请求头", 'status': False})

        token = auth[1]
        # 解密
        result = parse_payload(token)
        if not result['status']:
            return JsonResponse(result)
        # 将解密后数据赋值给user_info
        request.user_info = result['data']
