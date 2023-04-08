from uuid import uuid4

from api.v1.filters import TitleFilter
from api.v1.permissions import (AdminOrReadOnly, IsAdminUser,
                                IsUserWithPowerOrReadOnly)
from api.v1.serializers import (AdminSerializer, CategorySerializer,
                                CommentSerializer, CustomUserSerializer,
                                GenreSerializer, RegistrationSerializer,
                                ReviewSerializer, TitleReadSerializer,
                                TitleWriteSerializer, TokenObtainSerializer)
from django.core.mail import send_mail
from django.db.models import Avg
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from users.models import User


class TitleView(ModelViewSet):
    """
    Processing of the list `Title` objects.

    Endpoint `/api/v1/titles/`.
    """

    permission_classes = (AdminOrReadOnly,)
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).order_by(
        'year',
    )
    filter_backends = (DjangoFilterBackend,)
    ordering_fields = (
        'name',
        'year',
    )
    filterset_class = TitleFilter

    def update(self, *args: list, **kwargs: dict):
        """
        Deny access to the PUT method .

        Args:
            *args: not used.
            **kwargs: not used.

        Returns:
            MethodNotAllowed exception.

        """
        raise MethodNotAllowed('PUT', detail='Use PATCH')

    def partial_update(
        self,
        request: HttpRequest,
        *args: list,
        **kwargs: dict,
    ):
        """Override Partial Update Code if desired.

        Args:
            request: HTTPRequest.
            *args: not used.
            **kwargs: not used.

        Returns:
            Updated output.

        """
        return super().update(request, *args, **kwargs, partial=True)

    def get_serializer_class(self):
        """Call the desired serializer depending on the type of query.

        Returns:
            Desired serializer.
        """
        if self.action in (
            'list',
            'retrieve',
        ):
            return TitleReadSerializer
        return TitleWriteSerializer


class CGViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class CategoryView(CGViewSet):
    """
    Processing of the list `Category` objects.

    Endpoint `/api/v1/category/.
    """

    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer


class GenreView(CGViewSet):
    """
    Processing of the list `Genre` objects.

    Endpoint `/api/v1/genre/`
    """

    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsUserWithPowerOrReadOnly,)

    def get_title(self) -> Title:
        """
        Получаем объект `Title` по его `id`.

        Returns:
            Объект `Title`.
        """
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all().order_by('-pub_date')

    def perform_create(self, serializer: ReviewSerializer) -> None:
        serializer.save(title=self.get_title(), author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = (IsUserWithPowerOrReadOnly,)

    def perform_create(self, serializer: ReviewSerializer) -> None:
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(
            review=review,
            author=User.objects.get(pk=self.request.user.id),
        )

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all().order_by('-pub_date')


class CustomUserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        serializer = CustomUserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = CustomUserSerializer(
                request.user,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def api_token_for_user(request):
    serializer = TokenObtainSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        user = get_object_or_404(User, username=data.get('username'))
        serializer.filter_confirmation_code(
            user,
            data.get('confirmation_code'),
        )
        token = str(AccessToken.for_user(user))
        return Response(
            {
                'token': token,
            },
            status=status.HTTP_200_OK,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def api_registration(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    if not User.objects.filter(
        username=data.get('username'),
        email=data.get('email'),
    ).exists():
        serializer.filter_data(data)
    user, _ = User.objects.get_or_create(
        username=data.get('username'),
        email=data.get('email'),
    )
    confirmation_code = str(uuid4())
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        'Your confirmation_code',
        confirmation_code,
        None,
        [request.data['email']],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)
