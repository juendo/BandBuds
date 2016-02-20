from django.contrib import admin
from bba.models import Band, User, Liked_Band

class BandAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country','formed','genre')

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id','f_name','s_name','dob','smokes','gender','alcohol')

class LikedBandAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country','user_id')

admin.site.register(Band)
admin.site.register(User)
admin.site.register(Liked_Band)