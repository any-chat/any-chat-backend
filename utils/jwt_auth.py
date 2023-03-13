
import jwt
import datetime
from jwt import exceptions
from anychat.settings import SECRET_KEY, JWT_EXP


UserType = {'username': str, 'password': str}


def create_token(user: UserType, timeout=JWT_EXP) -> str:
    return jwt.encode({"username": user.username,
                       "iss": "anychat",
                       "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=int(timeout)),
                       "iat": datetime.datetime.utcnow(),
                       "nbf": datetime.datetime.utcnow() - datetime.timedelta(seconds=1)
                       }, key=SECRET_KEY)


def parse_payload(token):
    """
    用于解密
    :param token:
    :return:
    """
    result = {"status": False, "data": None, "error": None}
    try:
        # 进行解密
        verified_payload = jwt.decode(token, SECRET_KEY, issuer="anychat")
        result['status'] = True
        result['data'] = verified_payload
    except exceptions.ExpiredSignatureError:
        result['error'] = 'token已失效'
    except jwt.DecodeError:
        result['error'] = 'token认证失败'
    except jwt.InvalidTokenError:
        result['error'] = '非法的token'
    return result
