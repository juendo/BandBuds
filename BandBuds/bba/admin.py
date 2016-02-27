from django.contrib import admin
from bba.models import Band, User_Profile, Liked_Band, Buddy, Gig_Attendance

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
admin.site.register(User_Profile)
admin.site.register(Liked_Band)
admin.site.register(Buddy)
admin.site.register(Gig_Attendance)