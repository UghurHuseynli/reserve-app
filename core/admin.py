from django.contrib import admin
from .models import UserModel, RestaurantsModel, ReserveModel, FavoritiesModel, CommentsModel, DayModel, TimeModel

# Register your models here.
admin.site.register([UserModel, ReserveModel, FavoritiesModel, CommentsModel, DayModel, TimeModel])

class RestaurantsAdminModel(admin.ModelAdmin):
    readonly_fields = ('rate', )

admin.site.register(RestaurantsModel, RestaurantsAdminModel)
