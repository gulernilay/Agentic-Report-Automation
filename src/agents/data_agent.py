import requests
from typing import Any, Dict
from tenacity import retry, stop_after_attempt, wait_exponential
from ..utils.config import settings
from ..utils.logger import logger

# Authentication Endpoint
def _login_and_get_token() -> str:
    """Authenticate with the QueryRunner API and retrieve an access token.
    Returns:
        str: The access token received from the API.
    Raises:
        requests.exceptions.HTTPError: If the login request fails.
        RuntimeError: If the response doesn't contain an access token.
    """
    url = f"{settings.API_BASE_URL}{settings.API_LOGIN_PATH}"
    payload = {
        "username": settings.API_USERNAME,
        "password": settings.API_PASSWORD
    }
    logger.info("Logging in to QueryRunner API to fetch token...")
    resp = requests.post(url, json=payload, timeout=30)
    resp.raise_for_status()
    token = resp.json().get("access_token")
    if not token:
        raise RuntimeError("Login response did not include access_token")
    return token

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def fetch_data() -> Dict[str, Any]:
    """Fetch JSON data from QueryRunner API using either a static token or login flow."""
    token = settings.API_TOKEN or _login_and_get_token()
    url = f"{settings.API_BASE_URL}{settings.API_QUERY_PATH}"
    headers = {"Authorization": f"Bearer {token}"}
    body = {"key": settings.QUERY_KEY}

    logger.info(f"Fetching data from {url} with key='{settings.QUERY_KEY}'")
    resp = requests.post(url, headers=headers, json=body, timeout=60)
    if resp.status_code == 401 and not settings.API_TOKEN:
        # token may have expired; retry once with fresh login
        logger.warning("Unauthorized. Trying to refresh token...")
        token = _login_and_get_token()
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.post(url, headers=headers, json=body, timeout=60)

    resp.raise_for_status()
    data = resp.json()
    logger.info("Data fetched successfully.")
    return data

