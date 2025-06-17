import csv
import os
from typing import List
from core.schemas import Vacancy


class CSVManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.fieldnames = [
            'url', 'title', 'company', 'location', 'job_type',
            'workplace_type', 'experience_level', 'description',
            'salary', 'posted_date', 'applicant_count', 'view_count'
        ]
        self._initialize_csv()

    def _initialize_csv(self):
        """Create CSV file with headers if it doesn't exist"""
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        with open(self.filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()

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
