from django.shortcuts import render
import requests
from django import forms
from django.shortcuts import render
from .models import Repository  # Import the Repository model
from django.conf import settings



# Create your views here.
from .models import Repository

def home(request):
    return render(request, 'home.html')

def search(request):
    class SearchForm(forms.Form):
        query = forms.CharField(label='Search Repositories')

    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            search_query = form.cleaned_data.get('query')
            search_results = github_api_request(search_query)
            if search_results:
                # Save search results to database
                for result in search_results:
                    Repository.objects.create(
                        name=result['name'],
                        owner=result['owner']['login'],
                        description=result['description'],
                        stars=result['stargazers_count'],
                        forks=result['forks_count']
                    )
                return render(request, 'search_results.html', {'results': search_results})
            else:
                return render(request, 'error.html', {'message': 'Error fetching search results from GitHub API.'})
        # else:
        #     return render(request, 'error.html', {'message': 'Invalid search query.'})
    else:
        form = SearchForm()
    return render(request, 'search.html', {'form': form})

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

    response = requests.get(search_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return data.get('items', [])
    else:
        return None