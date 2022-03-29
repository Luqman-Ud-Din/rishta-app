from backend.users.serializers import CustomeTokenObtainPairSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt import (
    views as jwt_views, 
    exceptions as exp
    )

class OTPVALIDATE:
    pass

class CustomTokenViewBase(jwt_views.TokenViewBase):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except exp.TokenError as e:
            raise exp.InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class CustomeTokenObtainPairView(CustomTokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = CustomeTokenObtainPairSerializer

token_obtain_pair = CustomeTokenObtainPairView.as_view()