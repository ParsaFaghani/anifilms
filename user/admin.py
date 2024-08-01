from django.contrib import admin
from .models import Profile, Follow, Save, Subscription, DiscountCode

admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(Save)
admin.site.register(Subscription)
admin.site.register(DiscountCode)
