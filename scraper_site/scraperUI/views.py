from django.shortcuts import get_object_or_404, render

from .models import RedditSearchResult, RedditSearchTerm

# todo not all views are complete yet, I still need to add more documentations as well as finish results and add (might remove results in the end)

def index(request):
    most_recent_search_terms = RedditSearchTerm.objects.order_by('-date_searched').distinct()[:3]
    most_recent_searches = {}
    for search_term in most_recent_search_terms:
        most_recent_searches[search_term] = RedditSearchResult.objects.filter(search_term=search_term).order_by('-upvotes').distinct()[:4]
    return render(request, 'scraperUI/index.html', {'search_results': most_recent_searches})


def details(request, search_term_id):
    search_term = get_object_or_404(RedditSearchTerm, pk=search_term_id)
    top_results = RedditSearchResult.objects.filter(search_term=search_term_id).order_by('-upvotes')
    return render(request, 'scraperUI/details.html', {'search_term': search_term, 'top_results': top_results})

def results(request, search_term_id):
    return HttpResponse(f"You're looking at the search results for search term {search_term_id}")

def add(request, search_term_id):
    return HttpResponse(f"You are searching for {search_term_id} on reddit")
