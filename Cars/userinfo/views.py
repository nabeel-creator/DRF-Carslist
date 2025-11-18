from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from userinfo.api.serializer import RegestraSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# @api_view(['POST'])
# def logout_user(request):
#     request.user.auth.token.delete()
#     return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)  

# @api_view(['POST'])
# def register_user(request):
#     serializer = RegestraSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ViewUser(generics.RetrieveAPIView):
    serializer_class = RegestraSerializer

    def get_object(self):
        return self.request.user

class RegisterUser(generics.CreateAPIView):
    serializer_class = RegestraSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

class LogoutUser(generics.GenericAPIView):


    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
        except Exception:
            pass
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)