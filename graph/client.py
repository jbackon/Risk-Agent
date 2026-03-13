"""A HTTP layer that wraps all Microsoft Graph API calls."""

import os, httpx
from dotenv import load_dotenv
from pathlib import Path
from abc import ABC, abstractmethod
from msal import ConfidentialClientApplication

BASE_DIR = Path(__file__).resolve().parent.parent
env_path = Path(BASE_DIR / ".env")
load_dotenv(dotenv_path=env_path)

class AuthenticationStrategy(ABC):
    @abstractmethod
    def get_token(self) -> str:
        """A function for getting an API token"""
        pass

class GraphAuth(AuthenticationStrategy):
    def get_token(self) -> str:
        """A function for getting a token for the MS Graph API"""
        client_id = os.getenv("GRAPH_CLIENT_ID")
        client_secret = os.getenv("GRAPH_CLIENT_SECRET")
        tenant_id = os.getenv("GRAPH_TENANT_ID")

        GRAPH_AUTHORITY = os.getenv("GRAPH_AUTHORITY")
        authority = f"{GRAPH_AUTHORITY}/{tenant_id}"
        scope = [os.getenv("GRAPH_SCOPE")]

        app = ConfidentialClientApplication(
            client_id,
            authority=authority,
            client_credential=client_secret
        )
        token_response = app.acquire_token_for_client(scopes=scope)
        if token_response is None:
            raise RuntimeError("The token response returned a 'None' value.")
        elif 'error' in token_response: 
            raise RuntimeError(f"The token request returned an error: {token_response['error']}")
        else:
            access_token = token_response["access_token"]
            return access_token

class GraphClient:
    def __init__(self, base_url: str, strategy: AuthenticationStrategy) -> None:
        self.base_url = base_url
        self.strategy = strategy

    async def get_file_content(self, file_path: str) -> str:
        headers = {
            "authorization" : f"Bearer {self.strategy.get_token()}"
        }
        url = f"{self.base_url}/me/drive/root:/{file_path}:/content"
        async with httpx.AsyncClient(follow_redirects=True) as client:
            r = await client.get(url=url, headers=headers)
            r.raise_for_status()
            if r.text == "":
                raise RuntimeError(f"The API call returned no data. {r.status_code}")
            else:    
                data = r.text
                return data