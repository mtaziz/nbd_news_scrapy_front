from django.contrib import admin
from models import UserProfile


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_favorite_crawl_media_sort', 'user_favorite_crawl_media','user_favorite_crawl_dir_sort')
    list_per_page = 20
    readonly_fields = ('user_favorite_crawl_media_sort', 'user_favorite_crawl_media','user_favorite_crawl_dir_sort')


admin.site.register(UserProfile, UserProfileAdmin)