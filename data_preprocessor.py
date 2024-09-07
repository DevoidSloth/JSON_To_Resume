import spacy
from datetime import datetime
from num2words import num2words
import random

class DataPreprocessor:
    nlp = spacy.load("en_core_web_sm")

    @staticmethod
    def preprocess(data):
        # Ensure all expected sections are present
        sections = ['contact_details', 'skills', 'education', 'work_experience', 'volunteer_experience', 'certifications', 'awards']
        for section in sections:
            if section not in data:
                data[section] = []

        # Process summary
        if 'summary' in data:
            data['summary'] = DataPreprocessor.condense_summary(data['summary'])

        # Process skills
        if data['skills'] and isinstance(data['skills'][0], dict):
            # Skills are already in the correct format
            pass
        else:
            # Convert skills to the correct format
            data['skills'] = [{'name': skill, 'level': ''} for skill in data['skills']]

        # Process work experience
        for job in data['work_experience']:
            job['date'] = DataPreprocessor.format_date_range(job['date'])
            job['responsibilities'] = DataPreprocessor.quantify_achievements(job['responsibilities'])

        # Process education
        for edu in data['education']:
            edu['graduation_year'] = DataPreprocessor.format_year(edu['graduation_year'])

        # Process volunteer experience
        for volunteer in data['volunteer_experience']:
            volunteer['date'] = DataPreprocessor.format_date_range(volunteer['date'])

        # Process certifications
        data['certifications'] = [f"{cert} ({DataPreprocessor.format_year(datetime.now().year)})" for cert in data['certifications']]

        # Process awards
        for award in data['awards']:
            award['year'] = DataPreprocessor.format_year(award['year'])

        return data

    @staticmethod
    def condense_summary(summary):
        sentences = summary.split('.')
        return '. '.join(sentences[:3]) + '.'

    @staticmethod
    def format_date_range(date_range):
        start, end = date_range.split(' - ')
        return f"{DataPreprocessor.format_date(start)} - {DataPreprocessor.format_date(end)}"

    @staticmethod
    def format_date(date):
        if date.lower() == 'present':
            return date
        try:
            return datetime.strptime(date, '%Y').strftime('%m/%Y')
        except ValueError:
            return date

    @staticmethod
    def format_year(year):
        try:
            return datetime.strptime(str(year), '%Y').strftime('%Y')
        except ValueError:
            return str(year)

    @staticmethod
    def quantify_achievements(responsibilities):
        quantified = []
        for resp in responsibilities:
            doc = DataPreprocessor.nlp(resp)
            
            # Extract numerical values
            numbers = [token.text for token in doc if token.like_num]
            
            if numbers:
                # If numbers are present, use them in the quantification
                quantified.append(resp)
            else:
                # If no numbers are present, add a quantification based on the verb
                verb = DataPreprocessor.find_main_verb(doc)
                if verb:
                    quantity = DataPreprocessor.generate_quantity(verb.lemma_)
                    if quantity:
                        quantified.append(f"{resp}, {quantity}")
                    else:
                        quantified.append(resp)
                else:
                    quantified.append(resp)
        
        return quantified

    @staticmethod
    def find_main_verb(doc):
        for token in doc:
            if token.pos_ == "VERB":
                return token
        return None

    @staticmethod
    def generate_quantity(verb):
        """Generate a realistic quantity based on the verb."""
        verb_quantity_map = {
            "create": ("resulting in the creation of {value} new {metric}", "artworks", 3, 10),
            "exhibit": ("showcased in {value} {metric}", "galleries", 5, 15),
            "manage": ("overseeing a team of {value} {metric}", "professionals", 3, 10),
            "increase": ("leading to a {value}% increase in {metric}", "revenue", 10, 30),
            "decrease": ("achieving a {value}% reduction in {metric}", "costs", 10, 25),
            "improve": ("resulting in a {value}% improvement in {metric}", "efficiency", 15, 35),
            "reduce": ("cutting {metric} by {value}%", "processing time", 10, 30),
            "save": ("generating {value}% in {metric} savings", "annual", 5, 20),
            "generate": ("producing {value} new {metric}", "leads", 50, 200),
            "implement": ("successfully rolling out {value} new {metric}", "processes", 2, 5),
            "develop": ("creating {value} innovative {metric}", "features", 3, 8),
            "launch": ("initiating {value} successful {metric}", "campaigns", 2, 5),
            "lead": ("spearheading {value} major {metric}", "projects", 2, 5),
            "secure": ("obtaining {value} {metric}", "commissions", 2, 5),
            "complete": ("successfully delivering {value} {metric}", "projects", 2, 5)
        }

        if verb in verb_quantity_map:
            template, metric, min_val, max_val = verb_quantity_map[verb]
            value = random.randint(min_val, max_val)
            return template.format(value=value, metric=metric)
        else:
            return None