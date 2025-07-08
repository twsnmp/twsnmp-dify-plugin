import requests
import base64

class TwsnmpAPI:
    def __init__(self, url: str):
        """
        Initializes the TwsnmpAPI client.

        Args:
            url: The base URL of the TWSNMP API.
        """
        self.url = url
        self.token = ''

    def login(self, user: str, password: str) -> str:
        """
        Logs in to the TWSNMP API and retrieves an authentication token.

        Args:
            user: The user ID.
            password: The password.

        Returns:
            True if login is successful, False otherwise.
        """
        try:
            res = requests.post(
                f"{self.url}/login",
                json={"UserID": user, "Password": password},
                headers={'Content-Type': 'application/json'}
            )
            res.raise_for_status()  # Raise an exception for bad status codes
            r = res.json()
            if r and 'token' in r:
                self.token = r['token']
                return ""
            return "token not found"
        except requests.exceptions.RequestException as e:
            print(f"Login failed: {e}")
            return f"Login failed: {e}"

    def get(self, api: str):
        """
        Makes a GET request to a specified API endpoint.

        Args:
            api: The API endpoint path (e.g., '/api/v1/nodes').

        Returns:
            The response data in the specified format, or None on error.
        """
        try:
            res = requests.get(
                f"{self.url}{api}",
                headers={'Authorization': f'Bearer {self.token}'}
            )
            res.raise_for_status()            
            return res.json()
        except requests.exceptions.RequestException as e:
            print(f"GET request failed: {e}")
            return None

    def post(self, api: str, data: dict):
        """
        Makes a POST request to a specified API endpoint.

        Args:
            api: The API endpoint path.
            data: The JSON data to send in the request body.

        Returns:
            The JSON response as a dictionary, or None on error.
        """
        try:
            res = requests.post(
                f"{self.url}{api}",
                json=data,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.token}'
                }
            )
            res.raise_for_status()
            return res.json()
        except requests.exceptions.RequestException as e:
            print(f"POST request failed: {e}")
            return None

    def delete(self, api: str) -> bool:
        """
        Makes a DELETE request to a specified API endpoint.

        Args:
            api: The API endpoint path.

        Returns:
            True if the deletion is successful (status 204), False otherwise.
        """
        try:
            res = requests.delete(
                f"{self.url}{api}",
                headers={'Authorization': f'Bearer {self.token}'}
            )
            return res.status_code == 204
        except requests.exceptions.RequestException as e:
            print(f"DELETE request failed: {e}")
            return False
