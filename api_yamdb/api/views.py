import uuid

from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.permissions import (
    AdminModeratorAuthorPermission,
    AdminOnly,
    IsAdminUserOrReadOnly,
)
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    GetTokenSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleReadOnlySerializer,
    TitleSerializer,
    UserSerializer,
)
from api.mixins import CreateListDestroyViewSet
from reviews.models import Category, Genre, Review, Title, User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated, AdminOnly]
    lookup_field = 'username'
    filter_backends = [SearchFilter]
    search_fields = ['username']
    http_method_names = [
        'get',
        'post',
        'patch',
        'delete',
    ]

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='me'
    )
    def my_profile(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIGetToken(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        if not username:
            return Response(
                {'username': 'Имя пользователя обязательно!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = get_object_or_404(User, username=username)
        if not confirmation_code:
            return Response(
                {'confirmation_code': 'Код подтверждения обязателен!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if confirmation_code != user.confirmation_code:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = RefreshToken.for_user(user).access_token
        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class APISignup(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        confirmation_code = str(uuid.uuid3(uuid.NAMESPACE_DNS, username))
        try:
            user, created = User.objects.get_or_create(
                username=username,
                email=email
            )
        except IntegrityError:
            return Response(
                {'message': 'Пользователь с такими данными уже существует'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.confirmation_code = confirmation_code
        user.save()
        email_body = (
            f'Здравствуйте, {user.username}.'
            f'\nКод подтверждения для доступа к API: {user.confirmation_code}'
        )
        email = EmailMessage(
            subject='Код подтверждения для доступа к API!',
            body=email_body,
            to=[user.email],
        )
        email.send()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryCreateListDestroyViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreCreateListDestroyViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminUserOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleReadOnlySerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    @property
    def title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.title,
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    @property
    def review_for_comment(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.review_for_comment.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.review_for_comment,
        )
