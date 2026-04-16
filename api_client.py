import requests
from requests.exceptions import Timeout, HTTPError, RequestException

def fetch_data(url: str, headers: dict) -> requests.Response:
    try:
        # Add upper bound for time spent waiting. 
        response = requests.get(url, headers=headers, timeout=10)

        # Automatically throw an HTTPError if the status isn't 200 OK
        response.raise_for_status()

        # Success
        return response
    
    except Timeout:
        print(f"Timeout: Request for {url} took too long to respond")
        
    except HTTPError as e:
        print(f"HTTP Error. Details: {e}")
        
    except RequestException as e:
        print(f"Other Error: Details: {e}")
        
    # Exception has occurred
    return None