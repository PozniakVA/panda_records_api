from django.contrib import admin

from songs.models import Song


@admin.register(Song)
class UserAdmin(admin.ModelAdmin):
    pass
