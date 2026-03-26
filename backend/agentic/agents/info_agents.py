"""
Weather Agent - Provides weather information
News Agent - Provides news aggregation
"""
from typing import Dict, Any, Optional
from datetime import datetime
import os
import random
from .base_agent import BaseAgent, logger
import sys
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.api_clients import get_weather_client, get_news_client, get_auto_location, GeoLocationClient


class WeatherAgent(BaseAgent):
    """Agent specialized in weather information"""

    def __init__(self):
        super().__init__(
            name="Weather Agent",
            description="Provides current weather, forecasts, and weather alerts"
        )
        self.weather_client = get_weather_client()

    def can_handle(self, task: str) -> bool:
        """Check if this agent can handle the task"""
        weather_keywords = [
            "weather", "temperature", "forecast", "rain", "sunny",
            "climate", "humidity", "wind", "storm", "cold", "hot"
        ]
        task_lower = task.lower()
        return any(keyword in task_lower for keyword in weather_keywords)

    def _extract_location_from_task(self, task: str) -> Optional[str]:
        """Try to extract location from the task string"""
        task_lower = task.lower()

        # Common patterns for location extraction
        location_patterns = [
            "weather in ", "weather for ", "weather at ",
            "temperature in ", "temperature at ", "temperature for ",
            "forecast for ", "forecast in ",
            "rain in ", "rain at ",
        ]

        for pattern in location_patterns:
            if pattern in task_lower:
                # Extract everything after the pattern
                idx = task_lower.find(pattern)
                location = task[idx + len(pattern):].strip()
                # Clean up - remove trailing punctuation and common words
                location = location.rstrip('?.,!')
                for word in [' today', ' tomorrow', ' this week', ' now', ' right now']:
                    if location.lower().endswith(word):
                        location = location[:-len(word)].strip()
                if location:
                    return location

        return None

    async def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute weather-related tasks"""
        self.update_status("thinking", "Fetching weather data")

        try:
            # Try to extract location from the task itself first
            extracted_location = self._extract_location_from_task(task)

            if extracted_location:
                location = extracted_location
                logger.info(f"Extracted location from task: {location}")
            elif context.get("location"):
                location = context.get("location")
                logger.info(f"Using location from context: {location}")
            else:
                # Auto-detect location from IP
                logger.info("No location specified, auto-detecting from IP...")
                location = get_auto_location()
                logger.info(f"Auto-detected location: {location}")

            result = await self._get_weather(location)
            self.record_success()
            return result

        except Exception as e:
            self.record_failure(str(e))
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to fetch weather data"
            }

    async def _get_weather(self, location: str) -> Dict[str, Any]:
        """Get current weather and forecast"""
        self.update_status("active", f"Fetching weather for {location}")

        # Try to get real weather data
        real_weather = self.weather_client.get_current_weather(location)
        real_forecast = self.weather_client.get_forecast(location, days=3)

        if real_weather:
            # Use real API data
            logger.info(f"Using real weather data for {location}")
            current_weather = {
                "location": real_weather.get('location', location),
                "temperature": real_weather['temperature'],
                "feels_like": real_weather['feels_like'],
                "condition": real_weather['condition'],
                "humidity": real_weather['humidity'],
                "wind_speed": real_weather['wind_speed'],
                "timestamp": datetime.now().isoformat()
            }

            forecast = []
            if real_forecast and 'forecast' in real_forecast:
                for i, day_forecast in enumerate(real_forecast['forecast']):
                    day_name = ["Tomorrow", "Day After", "In 3 Days"][i] if i < 3 else f"In {i+1} Days"
                    forecast.append({
                        "day": day_name,
                        "high": day_forecast['high'],
                        "low": day_forecast['low'],
                        "condition": day_forecast['condition']
                    })

            return {
                "success": True,
                "agent": self.name,
                "action": "get_weather",
                "current": current_weather,
                "forecast": forecast,
                "source": "real_api",
                "message": f"Weather for {current_weather['location']}: {current_weather['temperature']}°C, {current_weather['condition']}"
            }
        else:
            # Fallback to simulated data
            logger.info(f"Using simulated weather data for {location}")
            conditions = ["Sunny", "Cloudy", "Partly Cloudy", "Rainy", "Clear", "Foggy"]
            current_weather = {
                "location": location,
                "temperature": random.randint(15, 30),
                "feels_like": random.randint(15, 30),
                "condition": random.choice(conditions),
                "humidity": random.randint(40, 80),
                "wind_speed": random.randint(5, 20),
                "timestamp": datetime.now().isoformat()
            }

            forecast = [
                {
                    "day": "Tomorrow",
                    "high": random.randint(20, 32),
                    "low": random.randint(10, 18),
                    "condition": random.choice(conditions)
                },
                {
                    "day": "Day After",
                    "high": random.randint(20, 32),
                    "low": random.randint(10, 18),
                    "condition": random.choice(conditions)
                },
                {
                    "day": "In 3 Days",
                    "high": random.randint(20, 32),
                    "low": random.randint(10, 18),
                    "condition": random.choice(conditions)
                }
            ]

            return {
                "success": True,
                "agent": self.name,
                "action": "get_weather",
                "current": current_weather,
                "forecast": forecast,
                "source": "simulated",
                "message": f"Weather for {location}: {current_weather['temperature']}°C, {current_weather['condition']} (simulated data)"
            }


class NewsAgent(BaseAgent):
    """Agent specialized in news aggregation"""

    def __init__(self):
        super().__init__(
            name="News Agent",
            description="Aggregates and provides latest news from various sources"
        )
        self.news_client = get_news_client()

    def can_handle(self, task: str) -> bool:
        """Check if this agent can handle the task"""
        news_keywords = [
            "news", "headline", "article", "latest news",
            "breaking news", "current events", "updates"
        ]
        task_lower = task.lower()
        return any(keyword in task_lower for keyword in news_keywords)

    async def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute news-related tasks"""
        self.update_status("thinking", "Fetching latest news")

        try:
            category = context.get("category", "general")
            result = await self._get_news(category)
            self.record_success()
            return result

        except Exception as e:
            self.record_failure(str(e))
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to fetch news"
            }

    async def _get_news(self, category: str) -> Dict[str, Any]:
        """Get latest news articles"""
        self.update_status("active", f"Fetching {category} news")

        # Try to get real news data
        real_news = self.news_client.get_top_headlines(category=category if category != 'general' else None, limit=5)

        if real_news and real_news.get('articles'):
            # Use real API data
            logger.info(f"Using real news data for category: {category}")
            return {
                "success": True,
                "agent": self.name,
                "action": "get_news",
                "category": category,
                "articles": real_news['articles'],
                "count": len(real_news['articles']),
                "total_available": real_news.get('total_results', 0),
                "source": "real_api",
                "message": f"Retrieved {len(real_news['articles'])} {category} news articles"
            }
        else:
            # Fallback to simulated data
            logger.info(f"Using simulated news data for category: {category}")
            articles = [
                {
                    "title": "Major Tech Breakthrough Announced",
                    "source": "Tech News",
                    "description": "A revolutionary advancement in AI technology...",
                    "url": "https://example.com/article1",
                    "published_at": datetime.now().isoformat()
                },
                {
                    "title": "Global Markets Show Strong Growth",
                    "source": "Financial Times",
                    "description": "Markets reached new highs today...",
                    "url": "https://example.com/article2",
                    "published_at": datetime.now().isoformat()
                },
                {
                    "title": "New Environmental Initiative Launched",
                    "source": "Green News",
                    "description": "A global initiative to combat climate change...",
                    "url": "https://example.com/article3",
                    "published_at": datetime.now().isoformat()
                },
                {
                    "title": "Scientific Discovery Changes Understanding",
                    "source": "Science Daily",
                    "description": "Researchers have made a groundbreaking discovery...",
                    "url": "https://example.com/article4",
                    "published_at": datetime.now().isoformat()
                },
                {
                    "title": "Sports Champions Celebrate Victory",
                    "source": "Sports Network",
                    "description": "The team secured their championship title...",
                    "url": "https://example.com/article5",
                    "published_at": datetime.now().isoformat()
                }
            ]

            return {
                "success": True,
                "agent": self.name,
                "action": "get_news",
                "category": category,
                "articles": articles,
                "count": len(articles),
                "source": "simulated",
                "message": f"Retrieved {len(articles)} {category} news articles (simulated data)"
            }
