"""
Utility modules for CoreAI
"""
from .oauth_helper import (
    GoogleOAuthHelper,
    oauth_helper,
    get_calendar_service,
    get_gmail_service
)
from .api_clients import (
    WeatherAPIClient,
    NewsAPIClient,
    GeoLocationClient,
    weather_client,
    news_client,
    geo_client,
    get_weather_client,
    get_news_client,
    get_geo_client,
    get_auto_location
)

__all__ = [
    'GoogleOAuthHelper',
    'oauth_helper',
    'get_calendar_service',
    'get_gmail_service',
    'WeatherAPIClient',
    'NewsAPIClient',
    'GeoLocationClient',
    'weather_client',
    'news_client',
    'geo_client',
    'get_weather_client',
    'get_news_client',
    'get_geo_client',
    'get_auto_location',
]
