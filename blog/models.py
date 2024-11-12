from django.conf import settings
from django.db import models
from django.utils import timezone
from markdownx.models import MarkdownxField  # Optional, if using markdownx
from django.utils.text import slugify
from django.utils.html import mark_safe
import markdown


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    content = MarkdownxField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
    def get_content_as_markdown(self):
        return mark_safe(markdown.markdown(
            self.content,
            extensions=[
                'markdown.extensions.fenced_code',
                'markdown.extensions.tables',
                'markdown.extensions.nl2br',
            ]
    ))

    def get_content_preview(self, length=300):
        # Convert markdown to plain text and truncate
        content = self.content[:length]
        if len(self.content) > length:
            content += '...'
        return mark_safe(markdown.markdown(content))
    
    def save(self, *args, **kwargs):
        if not self.slug:  # Only set the slug if it's not already set
            base_slug = slugify(self.title)
            unique_slug = base_slug
            num = 1
            # Keep checking until we find a unique slug
            while Post.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)