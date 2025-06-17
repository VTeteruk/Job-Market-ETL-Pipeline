import requests
import tqdm
from bs4 import BeautifulSoup
from typing import List

from core.config import configure_logging
from core.schemas import Vacancy
from core.csv_manager import CSVManager

from .job_card_scraper import JobCardScraper
from ..settings import HEADERS

logger = configure_logging()


class JobsScraper(JobCardScraper):
    def __init__(self, csv_filename: str):
        self.csv_manager = CSVManager(csv_filename)
        self.headers = HEADERS
        self.scraped_count = 0
        super().__init__()

    def fetch_url_content(self, url: str) -> str:
        return requests.request("GET", url, headers=self.headers).content

    def scrape_single_job(self, job_url: str) -> None:
        """Scrape a single job and save to CSV"""
        try:
            html_content = self.fetch_url_content(job_url)
            if not html_content:
                return

            soup = BeautifulSoup(html_content, "html.parser")
            job_data = self.extract_job_data(soup)

            vacancy = Vacancy(job_url, **job_data)
            self.csv_manager.save_vacancy(vacancy)
            self.scraped_count += 1

        except Exception as e:
            logger.error(f"Error scraping {job_url}: {e}")

    def scrape_jobs(self, job_urls: List[str]) -> None:
        for job_url in tqdm.tqdm(job_urls):
            self.scrape_single_job(job_url)
