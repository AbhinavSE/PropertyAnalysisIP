from .magicbricks import MagicbricksScraper
from ._99acres import _99acresScraper

if __name__ == '__main__':
    scraper = _99acresScraper()
    scraper.run()
