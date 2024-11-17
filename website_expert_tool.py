import requests
from bs4 import BeautifulSoup

class WebsiteExpertTool:
    def __init__(self):
        pass  # No initialization needed

    def get_expert_information(self, website, query):
        try:
            response = requests.get(website, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()  # Check for errors

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract information (Example: Extract the text content of the first paragraph)
            first_paragraph = soup.find('p').text  # Find the first paragraph

            return f"Information from website expert: {first_paragraph}"

        except requests.exceptions.RequestException as e:
            print(f"Error accessing website: {e}")
            return "Sorry, I couldn't access the website."