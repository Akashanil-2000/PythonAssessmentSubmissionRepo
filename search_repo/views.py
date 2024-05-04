# Import necessary modules
from django.shortcuts import render
from django import forms
from django.conf import settings
from .models import Repository
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Define a form for searching repositories
class SearchForm(forms.Form):
    query = forms.CharField(label='Search Repositories')


# Homepage view
def home(request):
    return render(request, 'home.html')


# Search view
def search(request):
    if request.method == 'GET':
        # Process GET request
        form = SearchForm(request.GET)
        if form.is_valid():
            # If form is valid, get search query and fetch results
            search_query = form.cleaned_data.get('query')
            search_results = github_api_request(search_query)
            if search_results:
                # If results are obtained, paginate and render search results
                paginator = Paginator(search_results, 10)  # 10 items per page
                page = request.GET.get('page')
                try:
                    results = paginator.page(page)
                except PageNotAnInteger:
                    results = paginator.page(1)
                except EmptyPage:
                    results = paginator.page(paginator.num_pages)

                # Save search results to the database
                save_search_results(search_results)

                return render(request, 'search_results.html', {'results': results, 'form': form})
            else:
                # If no results are obtained, render error message
                return render(request, 'error.html', {'message': 'Error fetching search results from GitHub API.'})
    else:
        # Process other request methods
        form = SearchForm()
    return render(request, 'search.html', {'form': form})


# Function to make request to GitHub API
def github_api_request(search_query):
    GITHUB_BASE_URL = 'https://api.github.com'
    search_url = f"{GITHUB_BASE_URL}/search/repositories"
    personal_access_token = settings.GITHUB_PERSONAL_ACCESS_TOKEN

    headers = {
        'Authorization': f"Bearer {personal_access_token}"
    }

    params = {
        'q': search_query
    }

    # Make GET request to GitHub API
    response = requests.get(search_url, headers=headers, params=params)

    if response.status_code == 200:
        # If request is successful, parse JSON response and return results
        data = response.json()
        return data.get('items', [])
    else:
        # If request fails, return None
        return None


# Function to save search results to the database
def save_search_results(search_results):
    for result in search_results:
        Repository.objects.create(
            name=result['name'],
            owner=result['owner']['login'],
            description=result['description'],
            stars=result['stargazers_count'],
            forks=result['forks_count']
        )
