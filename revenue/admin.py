from django.contrib import admin
from .models import Subscription, StreamRecord

# Register your models here.
admin.site.register(Subscription)
admin.site.register(StreamRecord)
