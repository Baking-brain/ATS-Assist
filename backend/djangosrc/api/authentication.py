from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken

class custom_jwtauthentication(JWTAuthentication):
    def authenticate(self, request):
        jwt_auth = JWTAuthentication()
        try:
            access_token = request.COOKIES.get('access_token')
            refresh_token = request.COOKIES.get('refresh_token')
            if not access_token or not refresh_token:
                return None
            validated_access_token = jwt_auth.get_validated_token(access_token)
            user = jwt_auth.get_user(validated_token=validated_access_token)

            request.user = user
            return (user, access_token)

        except Exception as e:
            #access token
            if 'expired' in str(e):
                # return Response({"status":"Access token expired"})
                raise InvalidToken("Access token is invalid or expired")
            else:
                raise InvalidToken('Something went wrong, access token')