import spacy
from datetime import datetime
from num2words import num2words
import random
from typing import Dict, List, Any, Optional
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

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
    def suggest_quantification(responsibility: str) -> str:
        doc = DataPreprocessor.nlp(responsibility)
        main_verb = DataPreprocessor.find_main_verb(doc)
        
        if main_verb:
            verb_text = main_verb.text.lower()
            suggestion = DataPreprocessor.get_custom_suggestion(verb_text, responsibility)
            return f"{Fore.YELLOW}Suggestion:{Style.RESET_ALL} {suggestion}\n{Fore.CYAN}Original:{Style.RESET_ALL} {responsibility}"
        
        return responsibility

    @staticmethod
    def get_custom_suggestion(verb: str, responsibility: str) -> str:
        suggestions = {
            "led": "Quantify the team's achievements. For example: 'Led a team of 5 developers, increasing productivity by 30% and delivering the project 2 weeks ahead of schedule.'",
            "implemented": "Measure the impact of the implementation. For instance: 'Implemented agile methodologies, reducing project delivery times by 25% and improving client satisfaction scores by 40%.'",
            "developed": "Highlight the scale and impact of your development work. Example: 'Developed RESTful APIs that increased mobile app performance by 50% and reduced server load by 30%.'",
            "mentored": "Quantify the impact of your mentoring. For example: 'Mentored 5 junior developers, leading to a 40% increase in their productivity within 6 months.'",
            "conducted": "Measure the outcomes of your reviews. For instance: 'Conducted code reviews that reduced bug rates by 35% and improved code quality scores by 28%.'",
            "collaborated": "Quantify the results of the collaboration. Example: 'Collaborated with the design team to implement UI improvements, resulting in a 20% increase in user engagement and a 15% decrease in bounce rate.'",
            "debugged": "Measure the impact of your debugging efforts. For instance: 'Debugged and resolved critical issues, reducing system downtime by 75% and saving the company an estimated $100,000 in potential revenue loss.'",
            "participated": "Quantify your contributions in meetings. For example: 'Participated in sprint planning and retrospectives, contributing ideas that led to a 25% increase in sprint velocity.'",
            "contributed": "Measure the impact of your contributions. For instance: 'Contributed to open-source projects, with pull requests that were merged into 5 major repositories and increased the projects' performance by an average of 15%.'",
        }
        
        return suggestions.get(verb, f"Consider adding measurable outcomes for '{verb}'. Include specific metrics such as percentage improvements, time saved, or quantifiable results achieved.")

    @staticmethod
    def quantify_achievements(responsibilities: List[str]) -> List[str]:
        quantified = []
        for resp in responsibilities:
            doc = DataPreprocessor.nlp(resp)
            
            # Extract numerical values
            numbers = [token.text for token in doc if token.like_num]
            
            if numbers:
                # If numbers are present, keep the original responsibility
                quantified.append(resp)
            else:
                # If no numbers are present, suggest adding metrics
                suggestion = DataPreprocessor.suggest_quantification(resp)
                print(f"\n{Back.WHITE}{Fore.BLACK}Achievement Quantification Suggestion:{Style.RESET_ALL}")
                print(suggestion)
                print(f"{Fore.GREEN}{'=' * 50}{Style.RESET_ALL}\n")
                quantified.append(resp)
        
        return quantified

    @staticmethod
    def find_main_verb(doc) -> Optional[spacy.tokens.Token]:
        for token in doc:
            if token.pos_ == "VERB":
                return token
        return None