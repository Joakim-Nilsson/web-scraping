from selectorlib import Extractor
import requests

class Temperature:
    """
    A scraper that uses an yml file to read the xpath of a value
    it needs to extract from the timeanddate.com/weather/url
    """

    headers = {
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent':
        'accept':

    }
    base_url = 'https://www.timeanddate.com/weather'
    yml_path = 'temperature.yaml'

    def __init__(self, country, city):
        self.country = country.replace(" ", "-")
        self.city = city.replace(" ", "-")

    def _build_url(self):
        url = self.base_url + self.country + "/" + self.city
        return url

    def _scrape(self):
        """Extracts a value as instructed by the yml file
        and returns a dictionary"""
        url = self._build_url()
        extractor = Extractor.from_yaml_file(self.yml_path)
        r = requests.get(url, headers=self.headers)
        full_content = r.text
        raw_content = extractor.extract(full_content)
        return raw_content

    def get(self):
        """Cleans the output of scrape"""
        scraped_content = self._scrape()
        return float(scraped_content['temp'].replace(""C","").strip())

print(__name__)
if __name__ == "__main__":
    temperature = Temperature(city="stockholm", country="Sweden")
    print(temperature.get())