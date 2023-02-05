from django.shortcuts import render, HttpResponse
import os
from pathlib import Path


# Create your views here.
def index(request):
    return HttpResponse('')

# from push_notifications.models import APNSDevice, GCMDevice

# device = GCMDevice.objects.get(registration_id=gcm_reg_id)

# # The first argument will be sent as "message" to the intent extras Bundle
# # Retrieve it with intent.getExtras().getString("message")

# device.send_message("You've got mail")

# # If you want to customize, send an extra dict and a None message.
# # the extras dict will be mapped into the intent extras Bundle.
# # For dicts where all values are keys this will be sent as url parameters,
# # but for more complex nested collections the extras dict will be sent via
# # the bulk message api.

# device.send_message(None, extra={"foo": "bar"})

# device = APNSDevice.objects.get(registration_id=apns_token)

# device.send_message("You've got mail") # Alert message may only be sent as text.

# device.send_message(None, badge=5) # No alerts but with badge.

# device.send_message(None, content_available=1, extra={"foo": "bar"}) # Silent message with custom data.
# # alert with title and body.

# device.send_message(message={"title" : "Game Request", "body" : "Bob wants to play poker"}, extra={"foo": "bar"})

# device.send_message("Hello again", thread_id="123", extra={"foo": "bar"}) # set thread-id to allow iOS to merge notifications