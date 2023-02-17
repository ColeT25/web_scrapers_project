from django.shortcuts import render

from .models import RedditSearchResult, RedditSearchTerm


def index(request):
    most_recent_search_terms = RedditSearchTerm.objects.order_by('-date_searched')[:2]
    most_recent_searches = RedditSearchResult.objects.filter(search_term__in=[term.id for term in most_recent_search_terms]).order_by('-upvotes')[:15]
    context = {'search_results': most_recent_searches}
    return render(request, 'scraperUI/index.html', context)


def details(request, search_term_id):
    return HttpResponse(f"You're looking at the search term details for {search_term_id}")


def results(request, search_term_id):
    return HttpResponse(f"You're looking at the search results for search term {search_term_id}")

def add(request, search_term_id):
    return HttpResponse(f"You are searching for {search_term_id} on reddit")
