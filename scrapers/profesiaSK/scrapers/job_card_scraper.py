import re

from bs4 import BeautifulSoup
from typing import Optional

from core.schemas import JobType, WorkplaceType, ExperienceLevel


def get_text_from_tag(tag) -> str:
    """Utility function to safely extract text from BeautifulSoup tag"""
    return tag.get_text(strip=True, separator="\n") if tag else ""


class JobCardScraper:
    @staticmethod
    def get_job_title(soup: BeautifulSoup) -> Optional[str]:
        try:
            return get_text_from_tag(soup.find("h1"))
        except Exception:
            return None

    @staticmethod
    def get_job_type(soup: BeautifulSoup) -> JobType:
        job_type_text = get_text_from_tag(soup.find("span", {"itemprop": "employmentType"}))

        # Map common Slovak job type terms to enum values
        type_mapping = {
            "plný úväzok": JobType.FULL_TIME,
            "full-time": JobType.FULL_TIME,
            "full time": JobType.FULL_TIME,
            "čiastočný úväzok": JobType.PART_TIME,
            "part-time": JobType.PART_TIME,
            "part time": JobType.PART_TIME,
            "zmluva": JobType.CONTRACT,
            "contract": JobType.CONTRACT,
            "stáž": JobType.INTERNSHIP,
            "internship": JobType.INTERNSHIP,
            "dočasný": JobType.TEMPORARY,
            "temporary": JobType.TEMPORARY,
            "freelance": JobType.FREELANCE,
        }

        for key, job_type in type_mapping.items():
            if key in job_type_text:
                return job_type

        return JobType.UNKNOWN  # Default

    def get_workplace_type(self, soup: BeautifulSoup) -> WorkplaceType:
        description = self.get_job_description(soup)

        # Map common terms to enum values
        if any(term in description for term in ["remote", "vzdialene", "home office"]):
            return WorkplaceType.REMOTE
        elif any(term in description for term in ["hybrid", "hybridny", "kombinovany"]):
            return WorkplaceType.HYBRID
        else:
            return WorkplaceType.ON_SITE

    def get_experience_level(self, soup: BeautifulSoup) -> Optional[ExperienceLevel]:
        description = self.get_job_description(soup)

        # Map common experience terms to enum values
        level_mapping = {
            "stáž": ExperienceLevel.INTERNSHIP,
            "internship": ExperienceLevel.INTERNSHIP,
            "junior": ExperienceLevel.ENTRY_LEVEL,
            "začiatočník": ExperienceLevel.ENTRY_LEVEL,
            "entry": ExperienceLevel.ENTRY_LEVEL,
            "medior": ExperienceLevel.ASSOCIATE,
            "associate": ExperienceLevel.ASSOCIATE,
            "senior": ExperienceLevel.MID_SENIOR,
            "mid": ExperienceLevel.MID_SENIOR,
            "lead": ExperienceLevel.DIRECTOR,
            "director": ExperienceLevel.DIRECTOR,
            "executive": ExperienceLevel.EXECUTIVE,
        }

        for key, level in level_mapping.items():
            if key in description:
                return level

        return None

    @staticmethod
    def get_job_description(soup: BeautifulSoup) -> Optional[str]:
        return get_text_from_tag(soup.find("div", {"class": "job-info details-section"})).replace(
            "Information about the position", ""
        )

    @staticmethod
    def get_job_salary(soup: BeautifulSoup) -> Optional[str]:
        return get_text_from_tag(soup.find("span", {"class": "salary-range d-block"}))

    @staticmethod
    def get_job_details(soup: BeautifulSoup) -> tuple:

        title, company, location, posted_date, salary = (None,) * 5

        elements = soup.find("div", {"class": "padding-on-bottom overall-info"})

        for element_name in elements.find_all("strong"):
            element_value = get_text_from_tag(element_name.find_next_sibling()).lower()
            element_name = get_text_from_tag(element_name).lower()

            try:
                if "dátum zverejnenia" in element_name and not posted_date:
                    posted_date = element_value
                elif "lokalita" in element_name and not location:
                    location = element_value.title()
                elif "spoločnosť" in element_name and not company:
                    company = element_value.title()
                elif "pozícia" in element_name and not title:
                    title = element_value.title()
            except Exception:
                continue

        try:
            salary = get_text_from_tag(elements).split(":")[-1].strip()
            if not re.findall(r"\d", salary):
                salary = None
        except Exception:
            pass

        return title, company, location, posted_date, salary

    @staticmethod
    def get_applicant_count(soup: BeautifulSoup) -> Optional[int]:
        return None

    @staticmethod
    def get_view_count(soup: BeautifulSoup) -> Optional[int]:
        return None

    def extract_job_data(self, soup: BeautifulSoup) -> dict:
        """Extract all job data from soup"""
        title, company, location, posted_date, salary = self.get_job_details(soup)
        best_title = self.get_job_title(soup)
        return {
            "title": best_title if best_title else title,
            "company": company,
            "location": location,
            "job_type": self.get_job_type(soup),
            "workplace_type": self.get_workplace_type(soup),
            "experience_level": self.get_experience_level(soup),
            "description": self.get_job_description(soup),
            "salary": salary,
            "posted_date": posted_date,
            "applicant_count": self.get_applicant_count(soup),
            "view_count": self.get_view_count(soup),
        }


if __name__ == "__main__":
    import requests
    s = JobCardScraper()
    sp = BeautifulSoup(requests.get("https://www.profesia.sk/praca/piano-software/O5096859?search_id=c90e8cd0-7bc3-4dd7-adf1-0a5aa6ad5f85", headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"}).content, "html.parser")
    print(sp)
    for key, value in s.extract_job_data(sp).items():
        print(f"{key}: {value}")