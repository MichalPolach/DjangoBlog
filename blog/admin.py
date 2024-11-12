from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['preview_content', 'created_date']
    list_filter = ('published_date', 'author')  # Adds filters in the sidebar
    search_fields = ('title', 'content')  # Adds search functionality
    date_hierarchy = 'published_date'  # Adds date-based navigation
    
    def preview_content(self, obj):
        return obj.get_content_as_markdown()
    preview_content.short_description = 'Content Preview'
    preview_content.allow_tags = True

admin.site.register(Post, PostAdmin)