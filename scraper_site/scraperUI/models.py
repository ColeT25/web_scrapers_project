import datetime

from django.db import models
from django.utils import timezone


class RedditSearchTerm(models.Model):
    searched_term = models.CharField(max_length=200)
    date_searched = models.DateTimeField('Date Searched')

    def __str__(self):
        return f'"{self.searched_term}" searched on {self.date_searched}'

    def was_searched_recently(self):
        return self.date_searched >= timezone.now() - datetime.timedelta(days=1)


class RedditSearchResult(models.Model):
    search_term = models.ForeignKey(RedditSearchTerm, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=200)
    author = models.CharField(max_length=30)
    subreddit = models.CharField(max_length=30)
    upvotes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    # todo add rewards field

    def __str__(self):
        return f'"{self.post_title}" by {self.author} on {self.subreddit}'
