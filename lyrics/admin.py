from django.contrib import admin
from .models import Post, Album, Artist


class PostAdmin(admin.ModelAdmin):
    list_display = ('artist', 'artists', 'title', 'albums', 'album', 'status')
    list_editable = ('status', 'artists', 'albums')
    list_filter = ('status', 'created', 'updated')
    search_fields = ('artists__artist_name', 'artist', 'title', 'albums__album')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created'
    list_per_page = 10


admin.site.register(Post, PostAdmin)
admin.site.register(Album)
admin.site.register(Artist)
# Register your models here.
