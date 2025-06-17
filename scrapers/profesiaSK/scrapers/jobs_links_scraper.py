import time

from bs4 import BeautifulSoup
from typing import List, Set

from core.config import configure_logging
from ..settings import BASE_URL, BASE_SEARCH_URL
from .jobs_scraper import JobsScraper


logger = configure_logging()


class JobsLinksScraper(JobsScraper):
    def __init__(self, csv_filename: str):
        super().__init__(csv_filename)
        self.collected_links: Set[str] = set()
        self.max_page_number = 10  # As then goes not relevant jobs

    def extract_job_links(self, page_url: str) -> List[str]:
        """Extract job links from a search results page"""
        self.headers['referer'] = page_url
        html_content = self.fetch_url_content(page_url)
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, "html.parser")
        return [
            BASE_URL[:-1] + container.find("h2").find("a").get("href")
            for container
            in soup.find_all("li", {"class": "list-row"})
        ]

    def scrape_all_pages(self) -> None:
        """Scrape job links from all pages and then scrape the jobs"""
        # Collect all job links
        page_num = 1
        while True:
            # Construct page URL
            page_url = BASE_SEARCH_URL.format(page_num)

            logger.info(f"Scraping page {page_num}")

            page_links = self.extract_job_links(page_url)

            if not page_links:
                break
            if page_num >= self.max_page_number:
                break

            self.scrape_jobs(page_links)

            page_num += 1

            # Add delay between page requests
            time.sleep(1)

