class DataPreprocessor:
    @staticmethod
    def preprocess(data):
        # Ensure all expected sections are present
        sections = ['contact_details', 'skills', 'education', 'work_experience', 'volunteer_experience', 'certifications', 'awards', 'extracurriculars']
        for section in sections:
            if section not in data:
                data[section] = []

        # Convert single strings to lists where needed
        list_fields = ['skills', 'certifications', 'awards']
        for field in list_fields:
            if isinstance(data[field], str):
                data[field] = [data[field]]

        return data

# Example usage:
# preprocessed_data = DataPreprocessor.preprocess(raw_data)