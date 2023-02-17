from django.contrib import admin

from .models import RedditSearchTerm, RedditSearchResult

admin.site.register(RedditSearchTerm)
admin.site.register(RedditSearchResult)
