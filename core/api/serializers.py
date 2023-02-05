from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import datetime, timedelta
from core.models import UserModel, RestaurantsModel, ReserveModel, FavoritiesModel, CommentsModel


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email

        return token

class ForgetSerializer(serializers.Serializer):
    email = serializers.EmailField()

class UserSerializerList(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        if obj.avatar:
            return f'{ obj.avatar.url }'
        return ''

    class Meta:
        model = UserModel
        fields = ['id', 'email', 'fullname', 'phone', 'avatar']

class UserSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email', 'fullname', 'phone', 'avatar', 'password']

    def create(self, validated_data):
        user = UserModel.objects.create(**validated_data, is_active = False)
        password = validated_data.pop('password')
        user.set_password(password)
        user.save()
        return user

class RestaurantSerializerList(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    opening_day = serializers.SerializerMethodField()
    avg_rate = serializers.SerializerMethodField()
    length_of_rate = serializers.SerializerMethodField()
    rate_list = serializers.SerializerMethodField()


    def get_opening_day(self, obj):
        return [ day.name for day in obj.opening_day.all() ]

    def get_image(self, obj):
        return f'{ obj.image.url }'
    
    def get_avg_rate(self, obj):
        return obj.rate
    
    def get_length_of_rate(self, obj):
        return obj.comments.all().count()
    
    def get_rate_list(self, obj):
        one_star = obj.comments.filter(rate = 1).all().count()
        two_star = obj.comments.filter(rate = 2).all().count()
        three_star = obj.comments.filter(rate = 3).all().count()
        four_star = obj.comments.filter(rate = 4).all().count()
        five_star = obj.comments.filter(rate = 5).all().count()
        rate_list = {
            '1 star': one_star,
            '2 star': two_star,
            '3 star': three_star,
            '4 star': four_star,
            '5 star': five_star
        }
        return rate_list

    class Meta:
        model = RestaurantsModel
        fields = ['id', 'name', 'image', 'avg_rate', 'address', 'opening_day', 'opening_hour', 'phone', 'email', 'discount', 'description', 'length_of_rate', 'rate_list']

class ReserveSerializerList(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    r_id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    def get_rate(self, obj):
        return obj.restaurant.rate
    
    def get_image(self, obj):
        return f'{ obj.restaurant.image.url }'
    
    def get_r_id(self, obj):
        return obj.restaurant.id
    
    def get_name(self, obj):
        return obj.restaurant.name

    def get_address(self, obj):
        return obj.restaurant.address

    class Meta:
        model = ReserveModel
        fields = ['time', 'guest', 'comment', 'rate', 'image', 'r_id', 'name', 'address', 'category']

class ReserveSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = ReserveModel
        fields = ['restaurant', 'time', 'guest', 'comment']
    
    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        reserve = ReserveModel.objects.create(**validated_data, user = user, category = 'Upcoming')
        reserve.save()
        return reserve

class FavoritieSerializerGet(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    r_id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_rate(self, obj):
        return obj.restaurant.rate
    
    def get_image(self, obj):
        return f'{ obj.restaurant.image.url }'
    
    def get_r_id(self, obj):
        return obj.restaurant.id
    
    def get_name(self, obj):
        return obj.restaurant.name

    class Meta:
        model = FavoritiesModel
        fields = ['user', 'rate', 'image', 'name', 'r_id']

class FavoritieSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = FavoritiesModel
        fields = ['user', 'restaurant']

class CommentSerializerList(serializers.ModelSerializer):
    time = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    def get_time(self, obj):
        created_at = datetime.strftime(obj.created_at, '%Y-%m-%d %H:%M')
        now = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M')
        time = datetime.strptime(now, '%Y-%m-%d %H:%M') - datetime.strptime(created_at, '%Y-%m-%d %H:%M')
        time = str(time).rsplit(':', 1)
        return time[0]

    def get_avatar(self, obj):
        if obj.user.avatar:
            return f'{ obj.user.avatar.url }'
        return ''

    class Meta:
        model = CommentsModel
        fields = ['id', 'restaurant', 'comments', 'rate', 'avatar', 'time']

class CommentSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = CommentsModel
        fields = ['restaurant', 'comments', 'rate']

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        comment = CommentsModel.objects.create(**validated_data, user = user)
        comment.save()
        return comment

        