import requests
from bs4 import BeautifulSoup

class WebsiteRAGTool:
    def __init__(self):
        pass  # No initialization required

    def extract_information(self, query, url=None):
        if not url:
            return "Please provide a URL for the website."
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()  # Check for errors

            soup = BeautifulSoup(response.content, 'html.parser')

            # Example Extraction: Look for a specific section 
            # (Adjust the selectors based on the target website's structure)
            content_section = soup.find('div', id='iphone-14-pro-features')
            if content_section:
                extracted_content = content_section.text
            else:
                extracted_content = "I couldn't find a section with specific features."

            return f"Extracted Information: {extracted_content}"

        except requests.exceptions.RequestException as e:
            print(f"Error accessing website: {e}")
            return "Sorry, I couldn't access the website."