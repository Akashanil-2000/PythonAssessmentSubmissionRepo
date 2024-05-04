from django.test import TestCase

# Create your tests here.
from .models import Repository
from .views import github_api_request, save_search_results

class RepositoryTestCase(TestCase):
    def setUp(self):
        # Set up test data
        self.repository = Repository.objects.create(
            name='Test Repository',
            owner='test_owner',
            description='Test repository description',
            stars=100,
            forks=50
        )

    def test_repository_creation(self):
        # Test if repository object is created successfully
        self.assertEqual(self.repository.name, 'Test Repository')
        self.assertEqual(self.repository.owner, 'test_owner')
        self.assertEqual(self.repository.description, 'Test repository description')
        self.assertEqual(self.repository.stars, 100)
        self.assertEqual(self.repository.forks, 50)

class GitHubAPITestCase(TestCase):
    def test_github_api_request(self):
        # Test GitHub API request function
        search_results = github_api_request('django')
        self.assertTrue(isinstance(search_results, list))

    def test_save_search_results(self):
        # Test saving search results to the database
        test_results = [
            {'name': 'Test Repository 1', 'owner': {'login': 'test_owner1'}, 'description': 'Description 1', 'stargazers_count': 10, 'forks_count': 5},
            {'name': 'Test Repository 2', 'owner': {'login': 'test_owner2'}, 'description': 'Description 2', 'stargazers_count': 20, 'forks_count': 10}
        ]
        save_search_results(test_results)
        self.assertEqual(Repository.objects.count(), 2)