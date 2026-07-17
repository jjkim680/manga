from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import urllib.parse

app = Flask(__name__)
# Allows your frontend (even if it's on a different local port or domain) to communicate with this backend
CORS(app) 

@app.route('/search', methods=['GET'])
def search_manga():
    # 1. Grab the search query sent from your JavaScript search bar
    query = request.args.get('text', '')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        # 2. Safely URL-encode the search query text
        encoded_query = urllib.parse.quote(query)
        url = f'https://weebcentral.com/search/data?author=&text={encoded_query}&sort=Best%20Match&order=Descending&official=Any&anime=Any&adult=Any&display_mode=Full%20Display'
        
        # 3. Perform the GET request (CORS restrictions do not apply to Python servers)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'} 
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            return jsonify({"error": f"Weebcentral returned status code {response.status_code}"}), 502

        # 4. Parse the returned HTML string
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the anchor tag containing the series link
        anchor_tag = soup.find('a', href=lambda href: href and '/series/' in href)
        
        if not anchor_tag:
            return jsonify({"error": "Manga link not found in search results"}), 404

        # Extract the URL (e.g., "https://weebcentral.com")
        href = anchor_tag['href']
        
        # Split the string to isolate the unique ID
        url_parts = href.split('/')
        manga_id = url_parts[4] 

        # 5. Send the extracted ID back to your JavaScript frontend as JSON data
        return jsonify({"mangaID": manga_id})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Starts the local development server on port 5000
    app.run(port=5000, debug=True)
