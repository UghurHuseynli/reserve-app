from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from datetime import datetime

# from django.contrib.gis.measure import D
# from django.contrib.gis.geos import GEOSGeometry, fromstr
# from django.contrib.gis.db.models.functions import Distance 
from geopy.distance import great_circle as GRC

from django.template.loader import render_to_string
from core.models import UserModel, RestaurantsModel, ReserveModel, FavoritiesModel, CommentsModel
from .serializers import RestaurantSerializerList, ReserveSerializerCreate, ReserveSerializerList, FavoritieSerializerGet, FavoritieSerializerPost, CommentSerializerCreate, CommentSerializerList, MyTokenObtainPairSerializer, UserSerializerCreate, UserSerializerList
from core.tokens import account_activation_token
from core.tasks import send_email_task


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class ActivateUserApi(APIView):
    def get(self, request, *args, **kwargs):
        User = UserModel
        uidb64 = kwargs['uidb64']
        token = kwargs['token']
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            return Response('Thank you for your email confirmation. Now you can login your account.', status=status.HTTP_200_OK)
        else:
            return Response('Activation link is invalid!', status=status.HTTP_406_NOT_ACCEPTABLE)

class ForgetApiView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        if email:
            if UserModel.objects.get(email = email):
                user = UserModel.objects.get(email = email)
                mail_subject = 'Reset your account password'
                message = render_to_string('password-reset.html', {
                    'user': user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.id)),
                    'token': account_activation_token.make_token(user),
                    'protocol': 'https' if request.is_secure() else 'http'
                })
                send_email_task.delay(mail_subject, message, email)
                return Response(f'A link has been sent to your {email} to reset your password, please go to the link.', status=status.HTTP_200_OK)
            return Response('This e-mail address does not exist in the system', status=status.HTTP_404_NOT_FOUND)
        return Response('Please enter your email address', status=status.HTTP_400_BAD_REQUEST)

class ResetApiView(APIView):
    def get(self, request, *args, **kwargs):
        User = UserModel
        uidb64 = kwargs['uidb64']
        token = kwargs['token']
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            return Response('Your account has been successfully activated', status=status.HTTP_202_ACCEPTED)


        return Response('Activation link is invalid!', status=status.HTTP_406_NOT_ACCEPTABLE)
    
    def post(self, request, *args, **kwargs):
        User = UserModel
        uidb64 = kwargs['uidb64']
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
        user.set_password(request.POST.get('password'))
        user.save()
        return Response('Your password has been successfully changed', status=status.HTTP_200_OK)
        
class UserViewSet(ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializerCreate
    permission_classes = []

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializerList
        return UserSerializerCreate

    def create(self, request, *args, **kwargs):
        many = True if isinstance(request.data, list) else False
        serializer = UserSerializerCreate(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        subject = 'Activate your account'
        message = render_to_string('user-activate.html', {
            'user': user,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.id)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http'
        })
        send_email_task.delay(subject, message, user.email)
        return Response(f'Your account has been created. Please activate your account by going to the activation link sent to your {serializer.data.get("email")} e-mail.', status=status.HTTP_201_CREATED)

class RestaurantViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = RestaurantsModel.objects.all()
    serializer_class = RestaurantSerializerList
    permission_classes = []

    def get_queryset(self):
        queryset =  super(RestaurantViewSet, self).get_queryset()

        name = self.request.GET.get('name')
        rate = self.request.GET.get('rate')
        nearby = self.request.GET.get('nearby')
        cuisine = self.request.GET.get('cuisine')
        discount = self.request.GET.get('discount')
        if name:
            queryset = queryset.filter(name = name).all()

        if rate:
            queryset = queryset.filter(rate__gte=rate)
        
        if cuisine:
            queryset = queryset.filter(cuisine = cuisine)
        
        if nearby:
            lat, lng, dist = nearby.split()
            dist = float(dist)
            user_location = (lat, lng)
            temp = []
            for query in queryset:
                res = GRC(user_location, (query.latitude, query.longtitude)).km
                if res <= dist:
                    temp.append(query.id)
            queryset = queryset.filter(id__in=temp)

        if discount and discount == 'true':
            queryset = queryset.exclude(discount__isnull=True).exclude(discount__exact='')
        
        if discount and discount == 'false':
            queryset = queryset.exclude(discount__isnull=False)

        return queryset

class ReserveViewSet(ModelViewSet):
    queryset = ReserveModel.objects.all()
    serializer_class = ReserveSerializerCreate
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReserveSerializerList
        return ReserveSerializerCreate
    
    def get_queryset(self):
        queryset = super(ReserveViewSet, self).get_queryset()

        user = self.request.user
        category = self.request.GET.get('category')


        if user:
            queryset = queryset.filter(user = user).all()

        if category:
            queryset = queryset.filter(category = category).all()

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        reserve = serializer.save()
        headers = self.get_success_headers(serializer.data)
        response = {
            'id': reserve.id,
            'Restaurant': reserve.restaurant.name,
            'Location': reserve.restaurant.address,
            'Date': datetime.strftime(reserve.time, '%d %b, %Y %H:%M'),
            'Guest': reserve.guest,
            'Description': reserve.comment
        }
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

class FavoritiesViewSet(ModelViewSet):
    queryset = FavoritiesModel.objects.all()
    serializer_class = FavoritieSerializerPost
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FavoritieSerializerGet
        return FavoritieSerializerPost

    def get_queryset(self):
        queryset = super(FavoritiesViewSet, self).get_queryset()

        user = self.request.GET.get('user')
        if user:
            queryset = queryset.filter(user = user).all()

        return queryset

class CommentViewSet(ModelViewSet):
    queryset = CommentsModel.objects.all()
    serializer_class = CommentSerializerCreate
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentSerializerList
        return CommentSerializerCreate

    def get_queryset(self):
        queryset = super(CommentViewSet, self).get_queryset()

        user = self.request.user
        restaurant = self.request.GET.get('restaurant')
        rate = self.request.GET.get('rate')

        if user:
            queryset = queryset.filter(user = user).all()

        if restaurant:
            queryset = queryset.filter(restaurant = restaurant).all()
        
        if rate:
            queryset = queryset.filter(rate__gte=rate).all()

        return queryset
