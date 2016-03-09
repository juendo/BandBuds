from django.contrib import admin
from bba.models import Band, UserProfile, LikedBand, Buddy, GigAttendance

class BandAdmin(admin.ModelAdmin):
    list_display = ('name', 'city','country','formed','genre')

class UserAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('user',)}

class BuddyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('user',)}

class GigAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('user',)}

class LikedBandAdmin(admin.ModelAdmin):
    list_display = ('band','user')


admin.site.register(Band)
admin.site.register(UserProfile)
admin.site.register(LikedBand)
admin.site.register(Buddy)
admin.site.register(GigAttendance)