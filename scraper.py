import requests
from bs4 import BeautifulSoup
import json
import os


"""     Har skrapat data från BBC artiklar, 1-3 om mat, 4-6 är om medicin, 7-9 är om rymden och 10 är om amerikanska valet
ytterst oklart om de kommer vara "olika nog" för testerna och att det ska bli tydligt. annars får vi göra om. """

# det man gör är att ändra texten nedan "article10.json" står det där nu, nästa blir 11 osv osv 
# sen ändrar man URL längre ner i koden. 


class NewsScraper:
    def __init__(self, url, output_folder="Data"):
        self.url = url
        # Define the output path in the "Data" folder
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the script's directory
        self.output_path = os.path.join(script_dir, output_folder, "article10.json")
        self.title = None
        self.text = None

        # Ensure the output folder exists
        os.makedirs(os.path.join(script_dir, output_folder), exist_ok=True)

    def fetch_content(self):
        """Fetches HTML content of the page."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Check if the request was successful
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the page: {e}")
            return None

    def parse_content(self, html_content):
        """Parses the HTML content to extract the title and text."""
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Extract title
        title_tag = soup.find("h1")
        self.title = title_tag.get_text().strip() if title_tag else "No title found"

        # Extract article text
        article_tag = soup.find("article")
        if article_tag:
            paragraphs = article_tag.find_all("p")
            self.text = "\n".join(p.get_text().strip() for p in paragraphs)
        else:
            self.text = "No article text found"

    def scrape_article(self):
        """Main method to scrape the article title and text, and save it to JSON."""
        html_content = self.fetch_content()
        if html_content:
            self.parse_content(html_content)
            self.save_to_json()

    def save_to_json(self):
        """Saves the article title and text to a JSON file with an ID."""
        
        # Load existing data if the JSON file already exists
        if os.path.exists(self.output_path):
            with open(self.output_path, "r", encoding="utf-8") as file:
                articles = json.load(file)
        else:
            articles = []
        
        # Assign a unique ID based on the current length of the list
        article_id = len(articles)

        # Create the article data structure
        article_data = {
            "id": article_id,
            "title": self.title,
            "text": self.text
        }

        # Append the new article to the list
        articles.append(article_data)

        # Save back to the JSON file
        with open(self.output_path, "w", encoding="utf-8") as file:
            json.dump(articles, file, ensure_ascii=False, indent=4)

# Example usage
url = "https://www.bbc.com/news/articles/clyg856px7eo"

scraper = NewsScraper(url)
scraper.scrape_article()
print(f"Article saved to {scraper.output_path}")
