import requests  # Import the requests library for web requests

class WebSearchTool:
    def __init__(self, api_key, search_engine_id):
        self.api_key = api_key
        self.search_engine_id = search_engine_id

    def search(self, query):
        # Implement web search using Google Custom Search API
        print(f"Performing web search for query: '{query}'")  # Debug statement
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": query
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            search_results = []
            for item in data.get('items', []):
                title = item.get('title')
                link = item.get('link')
                snippet = item.get('snippet')
                search_results.append(f"Title: {title}\nURL: {link}\nDescription: {snippet}\n")
            return "".join(search_results)  # Return a string of the search results
        else:
            print(f"Error performing web search: {response.status_code}")
            return ""