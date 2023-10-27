from django.contrib.auth import get_user_model
from django.core import validators
from django.db.models import Q
from rest_framework import status, viewsets, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.settings import api_settings
from .permissions import IsStaffOrSelf
from .serializers import CustomUserSerializer, CustomUserSimpleSerializer

# Create your views here.
class CustomUserList(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSimpleSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomUserIsStaff(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        isStaff = request.user.is_staff
        return Response({"isStaff": isStaff}, status=status.HTTP_200_OK)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    # pagination_class = CustomUserPagination
    permission_classes = [IsStaffOrSelf, permissions.IsAuthenticated]
    # basename = "customuser"

    # def get_queryset(self):
    #     query = self.request.GET.get('q', '')

    #     # Split the query into words to handle full names
    #     keywords = query.split()

    #     # Initialize an empty queryset
    #     queryset = get_user_model().objects.none()

    #     # Iterate through each keyword and filter the queryset
    #     for keyword in keywords:
    #         queryset |= get_user_model().objects.filter(
    #             Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword)
    #         )

    #     # Return the first 5 results
    #     return queryset[:5]


class LogoutView(views.APIView):

    def post(self, request, *args, **kwargs):
        response = Response({"message": "Logged out"}, status=status.HTTP_200_OK)
        return response
