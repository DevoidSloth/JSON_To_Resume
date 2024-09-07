from datetime import datetime

class DataPreprocessor:
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
        data['skills'] = [skill['name'] for skill in data['skills']]

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
        # This is a placeholder. In a real-world scenario, you might use NLP techniques
        # or a more sophisticated algorithm to quantify achievements.
        return [resp + " (quantified impact)" for resp in responsibilities]

# Example usage:
# preprocessed_data = DataPreprocessor.preprocess(raw_data)