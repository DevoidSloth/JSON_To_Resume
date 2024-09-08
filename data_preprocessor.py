import spacy
from datetime import datetime
from num2words import num2words
import random
from typing import Dict, List, Any, Optional

class DataPreprocessor:
    nlp = spacy.load("en_core_web_sm")

    @staticmethod
    def preprocess(data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            DataPreprocessor.ensure_sections(data)
            DataPreprocessor.process_summary(data)
            DataPreprocessor.process_skills(data)
            DataPreprocessor.process_work_experience(data)
            DataPreprocessor.process_education(data)
            DataPreprocessor.process_volunteer_experience(data)
            DataPreprocessor.process_certifications(data)
            DataPreprocessor.process_awards(data)
            return data
        except KeyError as e:
            raise KeyError(f"Missing required key in input data: {e}")
        except ValueError as e:
            raise ValueError(f"Invalid data format: {e}")

    @staticmethod
    def ensure_sections(data: Dict[str, Any]) -> None:
        sections = ['contact_details', 'skills', 'education', 'work_experience', 'volunteer_experience', 'certifications', 'awards']
        for section in sections:
            if section not in data:
                data[section] = []

    @staticmethod
    def process_summary(data: Dict[str, Any]) -> None:
        if 'summary' in data:
            data['summary'] = DataPreprocessor.condense_summary(data['summary'])

    @staticmethod
    def process_skills(data: Dict[str, Any]) -> None:
        if not data['skills']:
            return
        if isinstance(data['skills'][0], dict):
            return
        data['skills'] = [{'name': skill, 'level': ''} for skill in data['skills']]

    @staticmethod
    def process_work_experience(data: Dict[str, Any]) -> None:
        for job in data['work_experience']:
            job['date'] = DataPreprocessor.format_date_range(job['date'])
            job['responsibilities'] = DataPreprocessor.quantify_achievements(job['responsibilities'])

    @staticmethod
    def process_education(data: Dict[str, Any]) -> None:
        for edu in data['education']:
            edu['graduation_year'] = DataPreprocessor.format_year(edu['graduation_year'])

    @staticmethod
    def process_volunteer_experience(data: Dict[str, Any]) -> None:
        for volunteer in data['volunteer_experience']:
            volunteer['date'] = DataPreprocessor.format_date_range(volunteer['date'])

    @staticmethod
    def process_certifications(data: Dict[str, Any]) -> None:
        data['certifications'] = [f"{cert} ({DataPreprocessor.format_year(datetime.now().year)})" for cert in data['certifications']]

    @staticmethod
    def process_awards(data: Dict[str, Any]) -> None:
        for award in data['awards']:
            award['year'] = DataPreprocessor.format_year(award['year'])

    @staticmethod
    def condense_summary(summary: str) -> str:
        sentences = summary.split('.')
        return '. '.join(sentences[:3]) + '.'

    @staticmethod
    def format_date_range(date_range: str) -> str:
        start, end = date_range.split(' - ')
        return f"{DataPreprocessor.format_date(start)} - {DataPreprocessor.format_date(end)}"

    @staticmethod
    def format_date(date: str) -> str:
        if date.lower() == 'present':
            return date
        try:
            return datetime.strptime(date, '%Y').strftime('%m/%Y')
        except ValueError:
            return date

    @staticmethod
    def format_year(year: Any) -> str:
        try:
            return datetime.strptime(str(year), '%Y').strftime('%Y')
        except ValueError:
            return str(year)

    @staticmethod
    def quantify_achievements(responsibilities: List[str]) -> List[str]:
        quantified = []
        for resp in responsibilities:
            doc = DataPreprocessor.nlp(resp)
            
            # Extract numerical values
            numbers = [token.text for token in doc if token.like_num]
            
            if numbers:
                # If numbers are present, use them in the quantification
                quantified.append(resp)
            else:
                # If no numbers are present, keep the original responsibility without modification
                quantified.append(resp)
        
        return quantified

    @staticmethod
    def find_main_verb(doc) -> Optional[spacy.tokens.Token]:
        for token in doc:
            if token.pos_ == "VERB":
                return token
        return None