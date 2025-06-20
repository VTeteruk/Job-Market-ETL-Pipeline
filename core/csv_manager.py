import csv
import os
from typing import List

from core.config import configure_logging
from core.schemas import Vacancy


logger = configure_logging()


class CSVManager:
    def __init__(self, filename: str):
        self.filename = "/opt/airflow/project/" + filename
        self.fieldnames = [
            'url', 'title', 'company', 'location', 'job_type',
            'workplace_type', 'experience_level', 'description',
            'salary', 'posted_date', 'applicant_count', 'view_count'
        ]
        self._initialize_csv()

    def _initialize_csv(self):
        """Create CSV file with headers if it doesn't exist"""
        absolute_path = os.path.abspath(self.filename)
        logger.info(f"🔍 Initializing CSV file at: {absolute_path}")
        logger.info(f"📁 Directory: {os.path.dirname(absolute_path)}")
        logger.info(f"📄 Filename: {os.path.basename(absolute_path)}")
        logger.info(f"💻 Current working directory: {os.getcwd()}")

        # Створюємо директорію
        directory = os.path.dirname(self.filename)
        if directory:
            os.makedirs(directory, exist_ok=True)
            logger.info(f"📂 Directory created/verified: {os.path.abspath(directory)}")

        # Створюємо файл
        try:
            with open(self.filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()

            # Перевіряємо чи файл дійсно створився
            if os.path.exists(self.filename):
                file_size = os.path.getsize(self.filename)
                logger.info(f"✅ CSV file successfully created! Size: {file_size} bytes")
                logger.info(f"📊 File permissions: {oct(os.stat(self.filename).st_mode)[-3:]}")
            else:
                logger.error(f"❌ CSV file was not created at: {absolute_path}")

        except Exception as e:
            logger.error(f"💥 Error creating CSV file: {e}")
            raise

    def save_vacancy(self, vacancy: Vacancy):
        """Save a single vacancy to CSV"""
        with open(self.filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writerow(vacancy.to_dict())

    def save_vacancies(self, vacancies: List[Vacancy]):
        """Save multiple vacancies to CSV"""
        with open(self.filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            for vacancy in vacancies:
                writer.writerow(vacancy.to_dict())

    def get_vacancy_count(self) -> int:
        """Get the number of vacancies in the CSV file"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                return sum(1 for _ in reader) - 1  # Subtract header
        except FileNotFoundError:
            return 0
