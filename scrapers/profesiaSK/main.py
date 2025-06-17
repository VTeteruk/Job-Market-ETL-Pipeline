from core.settings import Settings
from core.config import configure_logging
from .scrapers.jobs_links_scraper import JobsLinksScraper

# Configure logging
logger = configure_logging()


def main():
    """Main scraping function"""
    logger.info("Starting Profesia.sk job scraping...")

    scraper = JobsLinksScraper(f"{Settings.SCRAPED_DATA_FOLDER}/profesia_sk_jobs.csv")

    try:
        scraper.scrape_all_pages()

        final_count = scraper.csv_manager.get_vacancy_count()
        logger.info(f"Scraping completed! Total jobs saved: {final_count}")

    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        raise


if __name__ == "__main__":
    main()
