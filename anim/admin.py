from django.contrib import admin
from .models import anim, anim_sub, anim_video


admin.site.register(anim)
admin.site.register(anim_video)
admin.site.register(anim_sub)
