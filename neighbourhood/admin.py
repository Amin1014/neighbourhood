from django.contrib import admin
from .models import Authorities, BlogPost, Business, Health, Profile, healthservices,neighbourhood, notifications
# Register your models here.
admin.site.register(Profile)
admin.site.register(neighbourhood)
admin.site.register(BlogPost)
admin.site.register(Business)
admin.site.register(Health)
admin.site.register(healthservices)
admin.site.register(Authorities)
admin.site.register(notifications)
