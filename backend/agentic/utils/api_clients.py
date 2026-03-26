"""
API Integration Helpers
Centralized API client management for external services
"""
import os
import requests
from typing import Dict, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class GeoLocationClient:
    """Client for IP-based geolocation"""

    _cached_location: Optional[Dict[str, Any]] = None

    @classmethod
    def get_location_from_ip(cls, ip_address: Optional[str] = None) -> Dict[str, Any]:
        """
        Get location from IP address using free IP geolocation APIs
        If no IP provided, uses the public IP of the server
        """
        # Return cached location if available
        if cls._cached_location and not ip_address:
            return cls._cached_location

        try:
            # Try ip-api.com (free, no key required, 45 requests/minute)
            if ip_address and ip_address not in ['127.0.0.1', 'localhost', '::1']:
                url = f"http://ip-api.com/json/{ip_address}"
            else:
                # Get public IP location
                url = "http://ip-api.com/json/"

            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            if data.get('status') == 'success':
                location = {
                    'city': data.get('city', 'Unknown'),
                    'region': data.get('regionName', ''),
                    'country': data.get('country', ''),
                    'country_code': data.get('countryCode', ''),
                    'latitude': data.get('lat'),
                    'longitude': data.get('lon'),
                    'timezone': data.get('timezone', ''),
                    'isp': data.get('isp', ''),
                    'query_ip': data.get('query', ip_address)
                }

                # Cache if it's the default location
                if not ip_address:
                    cls._cached_location = location

                logger.info(f"Detected location: {location['city']}, {location['country']}")
                return location
            else:
                logger.warning(f"IP geolocation failed: {data.get('message', 'Unknown error')}")

        except requests.exceptions.RequestException as e:
            logger.error(f"IP geolocation request failed: {str(e)}")
        except Exception as e:
            logger.error(f"IP geolocation error: {str(e)}")

        # Fallback: try ipinfo.io as backup
        try:
            if ip_address and ip_address not in ['127.0.0.1', 'localhost', '::1']:
                url = f"https://ipinfo.io/{ip_address}/json"
            else:
                url = "https://ipinfo.io/json"

            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            loc = data.get('loc', '0,0').split(',')
            location = {
                'city': data.get('city', 'Unknown'),
                'region': data.get('region', ''),
                'country': data.get('country', ''),
                'country_code': data.get('country', ''),
                'latitude': float(loc[0]) if len(loc) > 0 else 0,
                'longitude': float(loc[1]) if len(loc) > 1 else 0,
                'timezone': data.get('timezone', ''),
                'isp': data.get('org', ''),
                'query_ip': data.get('ip', ip_address)
            }

            if not ip_address:
                cls._cached_location = location

            logger.info(f"Detected location (backup): {location['city']}, {location['country']}")
            return location

        except Exception as e:
            logger.error(f"Backup IP geolocation also failed: {str(e)}")

        # Return default if all fails
        return {
            'city': 'Unknown',
            'region': '',
            'country': 'Unknown',
            'country_code': '',
            'latitude': 0,
            'longitude': 0,
            'timezone': '',
            'isp': '',
            'query_ip': ip_address
        }

    @classmethod
    def get_location_string(cls, ip_address: Optional[str] = None) -> str:
        """Get a simple location string like 'Mumbai, India'"""
        location = cls.get_location_from_ip(ip_address)
        if location['city'] != 'Unknown':
            return f"{location['city']}, {location['country']}"
        return "New York, US"  # Default fallback

    @classmethod
    def get_coordinates(cls, ip_address: Optional[str] = None) -> Tuple[float, float]:
        """Get latitude and longitude"""
        location = cls.get_location_from_ip(ip_address)
        return (location['latitude'], location['longitude'])


class WeatherAPIClient:
    """Unified client for weather APIs (OpenWeatherMap, WeatherAPI, etc.)"""

    def __init__(self):
        self.api_key = os.getenv('WEATHER_API_KEY')
        self.provider = os.getenv('WEATHER_API_PROVIDER', 'openweathermap')
        self.units = os.getenv('WEATHER_API_UNITS', 'metric')

    def get_current_weather(self, location: str) -> Optional[Dict[str, Any]]:
        """Get current weather for a location"""
        if not self.api_key or self.api_key == 'your_openweathermap_api_key':
            logger.info("Weather API key not configured, returning mock data")
            return None

        try:
            if self.provider == 'openweathermap':
                return self._get_openweathermap_current(location)
            elif self.provider == 'weatherapi':
                return self._get_weatherapi_current(location)
            else:
                logger.warning(f"Unknown weather provider: {self.provider}")
                return None
        except Exception as e:
            logger.error(f"Weather API error: {str(e)}")
            return None

    def _get_openweathermap_current(self, location: str) -> Dict[str, Any]:
        """Get weather from OpenWeatherMap"""
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': location,
            'appid': self.api_key,
            'units': self.units
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        return {
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'condition': data['weather'][0]['main'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'location': data['name']
        }

    def _get_weatherapi_current(self, location: str) -> Dict[str, Any]:
        """Get weather from WeatherAPI.com"""
        url = "https://api.weatherapi.com/v1/current.json"
        params = {
            'key': self.api_key,
            'q': location
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        return {
            'temperature': data['current']['temp_c'] if self.units == 'metric' else data['current']['temp_f'],
            'feels_like': data['current']['feelslike_c'] if self.units == 'metric' else data['current']['feelslike_f'],
            'condition': data['current']['condition']['text'],
            'humidity': data['current']['humidity'],
            'wind_speed': data['current']['wind_kph'] if self.units == 'metric' else data['current']['wind_mph'],
            'location': data['location']['name']
        }

    def get_forecast(self, location: str, days: int = 3) -> Optional[Dict[str, Any]]:
        """Get weather forecast"""
        if not self.api_key or self.api_key == 'your_openweathermap_api_key':
            return None

        try:
            if self.provider == 'openweathermap':
                return self._get_openweathermap_forecast(location, days)
            elif self.provider == 'weatherapi':
                return self._get_weatherapi_forecast(location, days)
        except Exception as e:
            logger.error(f"Weather forecast API error: {str(e)}")
            return None

    def _get_openweathermap_forecast(self, location: str, days: int) -> Dict[str, Any]:
        """Get forecast from OpenWeatherMap"""
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            'q': location,
            'appid': self.api_key,
            'units': self.units,
            'cnt': days * 8  # 8 forecasts per day (3-hour intervals)
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Group by day and get daily highs/lows
        forecast = []
        for i in range(0, len(data['list']), 8):
            day_data = data['list'][i:i+8]
            temps = [item['main']['temp'] for item in day_data]
            forecast.append({
                'high': max(temps),
                'low': min(temps),
                'condition': day_data[0]['weather'][0]['main']
            })

        return {'forecast': forecast[:days]}

    def _get_weatherapi_forecast(self, location: str, days: int) -> Dict[str, Any]:
        """Get forecast from WeatherAPI.com"""
        url = "https://api.weatherapi.com/v1/forecast.json"
        params = {
            'key': self.api_key,
            'q': location,
            'days': days
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        forecast = []
        for day in data['forecast']['forecastday']:
            forecast.append({
                'high': day['day']['maxtemp_c'] if self.units == 'metric' else day['day']['maxtemp_f'],
                'low': day['day']['mintemp_c'] if self.units == 'metric' else day['day']['mintemp_f'],
                'condition': day['day']['condition']['text']
            })

        return {'forecast': forecast}


class NewsAPIClient:
    """Client for News APIs - uses Serper (Google News) as primary, NewsAPI as fallback"""

    def __init__(self):
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.serper_api_key = os.getenv('SERPER_API_KEY')
        self.country = os.getenv('NEWS_API_COUNTRY', 'us')
        self.language = os.getenv('NEWS_API_LANGUAGE', 'en')

    def get_top_headlines(self, category: Optional[str] = None, limit: int = 5) -> Optional[Dict[str, Any]]:
        """Get top headlines - tries Serper first, then NewsAPI"""

        # Try Serper API first (works from server-side)
        if self.serper_api_key and self.serper_api_key != 'your_serper_api_key':
            result = self._get_serper_news(category, limit)
            if result:
                return result

        # Fallback to NewsAPI
        if self.news_api_key and self.news_api_key != 'your_newsapi_key':
            result = self._get_newsapi_headlines(category, limit)
            if result:
                return result

        logger.info("No news API configured or all APIs failed")
        return None

    def _get_serper_news(self, category: Optional[str] = None, limit: int = 5) -> Optional[Dict[str, Any]]:
        """Get news from Serper (Google News)"""
        try:
            url = "https://google.serper.dev/news"
            query = category if category and category != 'general' else "latest news today"

            headers = {
                'X-API-KEY': self.serper_api_key,
                'Content-Type': 'application/json'
            }

            payload = {
                'q': query,
                'gl': self.country,
                'hl': self.language,
                'num': limit
            }

            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            articles = []
            for item in data.get('news', [])[:limit]:
                articles.append({
                    'title': item.get('title', ''),
                    'description': item.get('snippet', ''),
                    'url': item.get('link', ''),
                    'source': item.get('source', 'Unknown'),
                    'published_at': item.get('date', ''),
                    'image_url': item.get('imageUrl')
                })

            if articles:
                logger.info(f"Got {len(articles)} articles from Serper API")
                return {
                    'articles': articles,
                    'total_results': len(articles)
                }

        except Exception as e:
            logger.error(f"Serper News API error: {str(e)}")

        return None

    def _get_newsapi_headlines(self, category: Optional[str] = None, limit: int = 5) -> Optional[Dict[str, Any]]:
        """Get headlines from NewsAPI (may not work from server on free tier)"""
        try:
            url = "https://newsapi.org/v2/top-headlines"
            params = {
                'apiKey': self.news_api_key,
                'country': self.country,
                'pageSize': limit
            }

            if category and category != 'general':
                params['category'] = category

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get('status') != 'ok':
                logger.warning(f"NewsAPI returned error: {data.get('message', 'Unknown')}")
                return None

            articles = []
            for article in data.get('articles', []):
                articles.append({
                    'title': article['title'],
                    'description': article.get('description', ''),
                    'url': article['url'],
                    'source': article['source']['name'],
                    'published_at': article['publishedAt'],
                    'image_url': article.get('urlToImage')
                })

            if articles:
                logger.info(f"Got {len(articles)} articles from NewsAPI")
                return {
                    'articles': articles,
                    'total_results': data.get('totalResults', 0)
                }

        except Exception as e:
            logger.error(f"NewsAPI error: {str(e)}")

        return None

    def search_news(self, query: str, limit: int = 5) -> Optional[Dict[str, Any]]:
        """Search news by keyword"""
        # Use Serper for search as it works better
        if self.serper_api_key and self.serper_api_key != 'your_serper_api_key':
            return self._get_serper_news(query, limit)
        return None


# Global instances
weather_client = WeatherAPIClient()
news_client = NewsAPIClient()
geo_client = GeoLocationClient()


def get_weather_client() -> WeatherAPIClient:
    """Get weather API client instance"""
    return weather_client


def get_news_client() -> NewsAPIClient:
    """Get news API client instance"""
    return news_client


def get_geo_client() -> GeoLocationClient:
    """Get geolocation client instance"""
    return geo_client


def get_auto_location() -> str:
    """Get user's location automatically via IP"""
    return GeoLocationClient.get_location_string()
