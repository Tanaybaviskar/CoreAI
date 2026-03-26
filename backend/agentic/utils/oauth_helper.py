"""
OAuth 2.0 Helper for Google APIs
Handles web-based authentication flow and token management
"""
import os
import json
import logging
from typing import Optional, Dict, Any
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)


class GoogleOAuthHelper:
    """Manages Google OAuth 2.0 web-based authentication and API access"""

    def __init__(self):
        self.client_id = os.getenv('GOOGLE_CLIENT_ID')
        self.client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        self.redirect_uri = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:5001/oauth/callback')

        # OAuth scopes - include openid and flexible order
        self.scopes = [
            'openid',  # Google automatically adds this, so include it
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/gmail.modify'
        ]

        # In-memory session storage (in production, use Redis/Database)
        self.user_sessions: Dict[str, Dict[str, Any]] = {}

    def is_configured(self) -> bool:
        """Check if OAuth is properly configured"""
        return bool(
            self.client_id and
            self.client_secret and
            self.client_id != 'your_client_id_from_oauth_credentials.json'
        )

    def get_authorization_url(self, state: str = None) -> Optional[str]:
        """Get the Google OAuth authorization URL for web flow"""
        if not self.is_configured():
            logger.warning("OAuth not configured")
            return None

        try:
            client_config = {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri]
                }
            }

            flow = Flow.from_client_config(
                client_config,
                scopes=self.scopes,
                redirect_uri=self.redirect_uri
            )

            auth_url, _ = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                prompt='consent',  # Force consent to get refresh token
                state=state
            )

            logger.info("Generated OAuth authorization URL")
            return auth_url

        except Exception as e:
            logger.error(f"Error creating authorization URL: {str(e)}")
            return None

    def exchange_code_for_tokens(self, auth_code: str) -> Optional[Dict[str, Any]]:
        """Exchange authorization code for tokens and user info"""
        if not self.is_configured():
            return None

        try:
            client_config = {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri]
                }
            }

            flow = Flow.from_client_config(
                client_config,
                scopes=self.scopes,
                redirect_uri=self.redirect_uri
            )

            # More flexible scope handling to avoid Google's automatic scope additions
            flow.redirect_uri = self.redirect_uri

            try:
                flow.fetch_token(code=auth_code)
            except Exception as scope_error:
                # If scope error, try with more flexibility
                logger.warning(f"Initial token exchange failed, trying flexible approach: {scope_error}")

                # Recreate flow with minimal scopes to get token first
                minimal_flow = Flow.from_client_config(
                    client_config,
                    scopes=['openid', 'email', 'profile'],  # Minimal scopes
                    redirect_uri=self.redirect_uri
                )
                minimal_flow.redirect_uri = self.redirect_uri
                minimal_flow.fetch_token(code=auth_code)
                credentials = minimal_flow.credentials

                # Log what scopes we actually got
                actual_scopes = list(credentials.scopes) if credentials.scopes else []
                logger.info(f"Successfully got token with scopes: {actual_scopes}")

                # Use these credentials even if scopes don't match exactly
                flow.credentials = credentials
            credentials = flow.credentials

            # Log successful scope acquisition
            actual_scopes = list(credentials.scopes) if credentials.scopes else []
            logger.info(f"OAuth completed successfully with scopes: {actual_scopes}")

            # Get user info
            user_info = self._get_user_info(credentials)

            token_data = {
                'access_token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_expiry': credentials.expiry.isoformat() if credentials.expiry else None,
                'user_info': user_info,
                'scopes': list(credentials.scopes) if credentials.scopes else self.scopes
            }

            # Store in session (use user email as key)
            user_email = user_info.get('email')
            if user_email:
                self.user_sessions[user_email] = token_data
                logger.info(f"Stored session for user: {user_email}")

            return token_data

        except Exception as e:
            logger.error(f"Error exchanging code for tokens: {str(e)}")
            return None

    def _get_user_info(self, credentials: Credentials) -> Dict[str, Any]:
        """Get user profile information"""
        try:
            service = build('oauth2', 'v2', credentials=credentials)
            user_info = service.userinfo().get().execute()

            return {
                'id': user_info.get('id'),
                'email': user_info.get('email'),
                'name': user_info.get('name'),
                'picture': user_info.get('picture'),
                'verified_email': user_info.get('verified_email', False)
            }
        except Exception as e:
            logger.error(f"Error getting user info: {str(e)}")
            return {}

    def get_user_session(self, user_email: str) -> Optional[Dict[str, Any]]:
        """Get stored user session data"""
        return self.user_sessions.get(user_email)

    def create_credentials_from_session(self, user_email: str) -> Optional[Credentials]:
        """Create Google credentials from stored session"""
        session_data = self.get_user_session(user_email)
        if not session_data:
            return None

        try:
            credentials = Credentials(
                token=session_data['access_token'],
                refresh_token=session_data.get('refresh_token'),
                token_uri="https://oauth2.googleapis.com/token",
                client_id=self.client_id,
                client_secret=self.client_secret,
                scopes=session_data.get('scopes', self.scopes)
            )

            # Check if token needs refresh
            if credentials.expired and credentials.refresh_token:
                logger.info(f"Refreshing token for user: {user_email}")
                request = Request()
                credentials.refresh(request)

                # Update session with new token
                session_data['access_token'] = credentials.token
                if credentials.expiry:
                    session_data['token_expiry'] = credentials.expiry.isoformat()
                self.user_sessions[user_email] = session_data

            return credentials

        except Exception as e:
            logger.error(f"Error creating credentials for {user_email}: {str(e)}")
            return None

    def get_calendar_service(self, user_email: str):
        """Get authenticated Google Calendar service for user"""
        credentials = self.create_credentials_from_session(user_email)
        if not credentials:
            return None

        try:
            service = build('calendar', 'v3', credentials=credentials)
            logger.info(f"Calendar service created for {user_email}")
            return service
        except Exception as e:
            logger.error(f"Failed to create Calendar service for {user_email}: {str(e)}")
            return None

    def get_gmail_service(self, user_email: str):
        """Get authenticated Gmail service for user"""
        credentials = self.create_credentials_from_session(user_email)
        if not credentials:
            return None

        try:
            service = build('gmail', 'v1', credentials=credentials)
            logger.info(f"Gmail service created for {user_email}")
            return service
        except Exception as e:
            logger.error(f"Failed to create Gmail service for {user_email}: {str(e)}")
            return None

    def revoke_user_session(self, user_email: str):
        """Revoke user session and delete stored tokens"""
        if user_email in self.user_sessions:
            del self.user_sessions[user_email]
            logger.info(f"Revoked session for user: {user_email}")

    def get_all_logged_in_users(self) -> list:
        """Get list of all logged-in users"""
        return list(self.user_sessions.keys())


# Global instance
oauth_helper = GoogleOAuthHelper()


def get_calendar_service(user_email: str):
    """Helper function to get Calendar service for user"""
    return oauth_helper.get_calendar_service(user_email)


def get_gmail_service(user_email: str):
    """Helper function to get Gmail service for user"""
    return oauth_helper.get_gmail_service(user_email)
