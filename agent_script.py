import os
import requests
from dotenv import load_dotenv

load_dotenv()

def main():

        print("Checking API credentials...\n")

       

        spotify_valid = check_spotify_credentials()

        groq_valid = check_groq_credentials()

       

        print(f"\nCredentials Summary:")

        print(f"Spotify: {'✅ Valid' if spotify_valid else '❌ Invalid'}")

        print(f"Groq: {'✅ Valid' if groq_valid else '❌ Invalid'}")

       

        if spotify_valid and groq_valid:

            print("\n🎉 All credentials are working!")

        else:

            print("\n⚠️  Please fix invalid credentials before proceeding.")

def check_spotify_credentials():

    """

    Check if Spotify API credentials are valid by attempting to get an access token.

    Returns True if valid, False otherwise.

    """

    client_id = os.getenv("SPOTIFY_CLIENT_ID")

    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

    

    # Check if credentials exist

    if not all([client_id, client_secret, redirect_uri]):

        print("❌ Missing Spotify credentials in .env file")

        return False

    

    # Test credentials by requesting a client credentials token

    auth_url = "https://accounts.spotify.com/api/token"

    auth_headers = {

        "Content-Type": "application/x-www-form-urlencoded"

    }

    auth_data = {

        "grant_type": "client_credentials",

        "client_id": client_id,

        "client_secret": client_secret

    }

    

    try:

        response = requests.post(auth_url, headers=auth_headers, data=auth_data)

        if response.status_code == 200:

            print("✅ Spotify credentials are valid")

            return True

        else:

            print(f"❌ Spotify credentials invalid. Status: {response.status_code}")

            print(f"Response: {response.json()}")

            return False

    except Exception as e:

        print(f"❌ Error checking Spotify credentials: {e}")

        return False

    
def check_groq_credentials():
    """
    Check if Groq API credentials are valid by attempting to get an access token.

    Returns True if valid, False otherwise.

    """
    api_key = os.getenv("GROQ_API_KEY")

    

    # Check if credentials exist

    if not api_key:

        print("❌ Missing Spotify credentials in .env file")

        return False

    

    # Test credentials by requesting a client credentials token

    auth_url = "https://api.groq.com/openai/v1/models"

    auth_headers = {

        "Authorization": f"Bearer {api_key}"

    }

    

    try:

        response = requests.get(auth_url, headers=auth_headers)

        if response.status_code == 200:

            print("✅ Groq credentials are valid")

            return True

        else:

            print(f"❌ Groq credentials invalid. Status: {response.status_code}")

            print(f"Response: {response.json()}")

            return False

    except Exception as e:

        print(f"❌ Error checking Groq credentials: {e}")

        return False

if __name__ == "__main__":
    main()