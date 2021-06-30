from user.permissions import IsActive
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from user.serializers import VirtueleTokenObtainPairSerializer
from product.models import Review
from product.serializers import ReviewSerializer

class VirtueleTokenObtainPairView(TokenObtainPairView):
    """
    Generate JWT Token

    Return two kinds of token if authentication is succesful.<br>
    The access token will valid for 30 minutes, while the refresh for 7 days.<br>
    Use the access token as an authorization for any protected API.
    """

    serializer_class = VirtueleTokenObtainPairSerializer
    
    @swagger_auto_schema(
        request_body=VirtueleTokenObtainPairSerializer(),
        responses={
            200: openapi.Schema(type=openapi.TYPE_OBJECT, properties={'access': 'Access Token', 'refresh': 'Refresh Token'}),
            401: 'Invalid User\'s Credential'
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class VirtueleTokenRefreshView(TokenRefreshView):
    """
    Refresh Access Token

    Use the refresh token to generate a new valid access token.
    """

    @swagger_auto_schema(
        request_body=TokenRefreshSerializer(),
        responses={
            200: openapi.Schema(type=openapi.TYPE_OBJECT, properties={'access': 'Access Token'}),
            400: 'Invalid Refresh Token'
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except:
            raise InvalidToken(args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class UserReviews(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={
            200: ReviewSerializer(many=True),
            204: 'No Content',
            401: 'Invalid User\'s Credential',
        }
    )
    def get(self, request, id):
        """
        User Reviews

        Return a list of user's reviews with mentioned ID.
        Return 401 if the request are not authenticated (user aren't logged in).
        You can set a GET parameter list to filter the result.<br>
        **product**: Returned review will be on product with mentioned slug only.
        """
        
        reviews = Review.objects.filter(user__id=id)

        if request.GET.get('product'):
            reviews.filter(product__slug=request.GET.get('product'))

        if not reviews:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class MyReviews(APIView):
    permission_classes = [IsActive]

    @swagger_auto_schema(
        responses={
            200: ReviewSerializer(many=True),
            204: 'No Content',
            401: 'Invalid User\'s Credential',
        }
    )
    def get(self, request):
        """
        My Reviews

        Return a list of requesting user's review.
        Return 401 if the request are not authenticated (user aren't logged in).
        You can set a GET parameter list to filter the result.<br>
        **product**: Returned review will be on product with mentioned slug only.
        """

        reviews = Review.objects.filter(user=request.user)

        if request.GET.get('product'):
            reviews.filter(product__slug=request.GET.get('product'))

        if not reviews:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)