from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CommentsModel, RestaurantsModel

@receiver([post_save, post_delete], sender = CommentsModel)
def rate(sender, instance, *args, **kwargs):
    restaurant = RestaurantsModel.objects.get(id = instance.restaurant.id)
    rate = [ obj.rate for obj in CommentsModel.objects.filter(restaurant = instance.restaurant.id) ]
    if rate:
        restaurant.rate = sum(rate) / len(rate)
    else:
        restaurant.rate = 0
    restaurant.save()
