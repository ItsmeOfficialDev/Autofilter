import requests
import time
from config import Config
import logging

logger = logging.getLogger(__name__)

class TMDBHandler:
    def __init__(self):
        self.api_key = Config.TMDB_API_KEY
        self.base_url = "https://api.themoviedb.org/3"
        self.image_base_url = "https://image.tmdb.org/t/p/w500"
        self.delay = Config.DELAY_BETWEEN_REQUESTS
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json;charset=utf-8'
        })
    
    def make_request(self, endpoint, params=None):
        time.sleep(self.delay)
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"TMDB API error: {e}")
            return None
    
    def discover_movies(self, language, page=1, year=None):
        params = {
            'with_original_language': language,
            'page': page,
            'sort_by': 'popularity.desc',
            'include_adult': False
        }
        if year:
            params['primary_release_year'] = year
        return self.make_request('discover/movie', params)
    
    def get_movie_details(self, movie_id):
        return self.make_request(f'movie/{movie_id}')
    
    def get_movie_poster(self, poster_path):
        if poster_path:
            return f"{self.image_base_url}{poster_path}"
        return None
    
    def search_movies_by_year_range(self, language, start_year=1950, end_year=2024):
        all_movies = []
        for year in range(start_year, end_year + 1):
            page = 1
            while True:
                data = self.discover_movies(language, page, year)
                if not data or 'results' not in data:
                    break
                movies = data['results']
                if not movies:
                    break
                all_movies.extend(movies)
                if page >= data.get('total_pages', 1) or page >= 10:
                    break
                page += 1
            logger.info(f"Fetched {len(all_movies)} movies for {language} up to {year}")
        return all_movies
