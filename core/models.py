from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from .managers import CustomUserManager

# Create your models here.

class UserModel(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=60)
    phone = models.CharField(max_length=14)
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email

class TimeModel(models.Model):
    time = models.CharField(max_length=15)

    def __str__(self):
        return self.time

class DayModel(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

HOUR_CHOICES = (
    ('07:00 - 18:00','07:00 - 18:00'),
    ('08:00 - 18:00','08:00 - 18:00'),
    ('09:00 - 18:00', '09:00 - 18:00'),
    ('10:00 - 18:00','10:00 - 18:00'),
    ('11:00 - 18:00','11:00 - 18:00'),
    ('07:00 - 19:00','07:00 - 19:00'),
    ('08:00 - 19:00','08:00 - 19:00'),
    ('09:00 - 19:00', '09:00 - 19:00'),
    ('10:00 - 19:00','10:00 - 19:00'),
    ('11:00 - 19:00','11:00 - 19:00'),
    ('07:00 - 20:00','07:00 - 20:00'),
    ('08:00 - 20:00','08:00 - 20:00'),
    ('09:00 - 20:00', '09:00 - 20:00'),
    ('10:00 - 20:00','10:00 - 20:00'),
    ('11:00 - 20:00','11:00 - 20:00'),
    ('07:00 - 21:00','07:00 - 21:00'),
    ('08:00 - 21:00','08:00 - 21:00'),
    ('09:00 - 21:00', '09:00 - 21:00'),
    ('10:00 - 21:00','10:00 - 21:00'),
    ('11:00 - 21:00','11:00 - 21:00'),
    ('07:00 - 22:00','07:00 - 22:00'),
    ('08:00 - 22:00','08:00 - 22:00'),
    ('09:00 - 22:00', '09:00 - 22:00'),
    ('10:00 - 22:00','10:00 - 22:00'),
    ('11:00 - 22:00','11:00 - 22:00'),
    ('07:00 - 23:00','07:00 - 23:00'),
    ('08:00 - 23:00','08:00 - 23:00'),
    ('09:00 - 23:00', '09:00 - 23:00'),
    ('10:00 - 23:00','10:00 - 23:00'),
    ('11:00 - 23:00','11:00 - 23:00'),
    ('07:00 - 01:00','07:00 - 01:00'),
    ('08:00 - 01:00','08:00 - 01:00'),
    ('09:00 - 01:00', '09:00 - 01:00'),
    ('10:00 - 01:00','10:00 - 01:00'),
    ('11:00 - 01:00','11:00 - 01:00'),
)

TYPE_CHOICES = (
    ('Italian', 'Italian'),
    ('China', 'China'),
    ('Azerbaijan', 'Azerbaijan'),
    ('India', 'India'),

)

CATEGORY_CHOICES = (
    ('Upcoming', 'Upcoming'),
    ('Past', 'Past'),
    ('Cancelled', 'Cancelled')
)

class RestaurantsModel(models.Model):
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to='restaurant/')
    rate = models.FloatField(null=True, blank=True, default=0.0)
    longtitude = models.CharField(max_length=15)
    latitude = models.CharField(max_length=15)
    address = models.CharField(max_length=300)
    opening_day = models.ManyToManyField(DayModel)
    opening_hour = models.CharField(max_length=25, choices=HOUR_CHOICES, default='09:00 - 23:00')
    phone = models.CharField(max_length=14)
    email = models.EmailField(unique=True, null=True, blank=True)
    discount = models.CharField(max_length=2000, null=True, blank=True)
    cuisine = models.CharField(max_length=30, choices=TYPE_CHOICES, default='Azerbaijan')
    description = models.CharField(max_length=2000)

    def __str__(self) -> str:
        return self.name

class ReserveModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(RestaurantsModel, on_delete=models.CASCADE)
    time = models.DateTimeField()
    guest = models.IntegerField()
    comment = models.CharField(max_length=1000, null=True, blank=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Upcoming')

    def __str__(self) -> str:
        return f'{self.id} -- {self.user}'

class FavoritiesModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(RestaurantsModel, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.id} -- {self.user}'

class CommentsModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(RestaurantsModel, on_delete=models.CASCADE, related_name='comments')
    comments = models.TextField()
    rate = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.id} -- {self.user}'