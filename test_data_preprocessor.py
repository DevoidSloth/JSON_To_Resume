import pytest
from data_preprocessor import DataPreprocessor
from datetime import datetime

@pytest.fixture
def sample_data():
    return {
        "summary": "Experienced software developer with expertise in Python and web technologies. Passionate about creating efficient and scalable solutions. Skilled in agile methodologies and team collaboration.",
        "skills": ["Python", "JavaScript", "SQL", "Docker"],
        "education": [
            {
                "degree": "Bachelor of Science in Computer Science",
                "institution": "University of Technology",
                "graduation_year": 2020
            }
        ],
        "work_experience": [
            {
                "title": "Software Developer",
                "company": "Tech Solutions Inc.",
                "date": "2020 - Present",
                "responsibilities": [
                    "Developed RESTful APIs for mobile applications",
                    "Implemented CI/CD pipelines for automated testing and deployment",
                    "Collaborated with cross-functional teams to deliver high-quality software"
                ]
            }
        ],
        "volunteer_experience": [
            {
                "organization": "Code for Good",
                "role": "Volunteer Developer",
                "date": "2019 - 2020"
            }
        ],
        "certifications": ["AWS Certified Developer", "Certified Scrum Master"],
        "awards": [
            {
                "title": "Best Innovation Award",
                "year": 2021
            }
        ]
    }

def test_preprocess(sample_data):
    processed_data = DataPreprocessor.preprocess(sample_data)
    assert isinstance(processed_data, dict)
    assert all(section in processed_data for section in ['contact_details', 'skills', 'education', 'work_experience', 'volunteer_experience', 'certifications', 'awards'])

def test_ensure_sections(sample_data):
    DataPreprocessor.ensure_sections(sample_data)
    assert all(section in sample_data for section in ['contact_details', 'skills', 'education', 'work_experience', 'volunteer_experience', 'certifications', 'awards'])

def test_process_summary(sample_data):
    DataPreprocessor.process_summary(sample_data)
    assert len(sample_data['summary'].split('.')) <= 4

def test_process_skills(sample_data):
    DataPreprocessor.process_skills(sample_data)
    assert all(isinstance(skill, dict) for skill in sample_data['skills'])
    assert all('name' in skill and 'level' in skill for skill in sample_data['skills'])

def test_process_work_experience(sample_data):
    DataPreprocessor.process_work_experience(sample_data)
    for job in sample_data['work_experience']:
        assert ' - ' in job['date']
        assert all(isinstance(resp, str) for resp in job['responsibilities'])

def test_process_education(sample_data):
    DataPreprocessor.process_education(sample_data)
    for edu in sample_data['education']:
        assert isinstance(edu['graduation_year'], str)
        assert len(edu['graduation_year']) == 4

def test_process_volunteer_experience(sample_data):
    DataPreprocessor.process_volunteer_experience(sample_data)
    for volunteer in sample_data['volunteer_experience']:
        assert ' - ' in volunteer['date']

def test_process_certifications(sample_data):
    DataPreprocessor.process_certifications(sample_data)
    assert all('(' in cert and ')' in cert for cert in sample_data['certifications'])

def test_process_awards(sample_data):
    DataPreprocessor.process_awards(sample_data)
    for award in sample_data['awards']:
        assert isinstance(award['year'], str)
        assert len(award['year']) == 4

def test_condense_summary():
    long_summary = "This is the first sentence. This is the second sentence. This is the third sentence. This is the fourth sentence. This is the fifth sentence."
    condensed = DataPreprocessor.condense_summary(long_summary)
    assert len(condensed.split('.')) <= 4

def test_format_date_range():
    date_range = "2020 - Present"
    formatted = DataPreprocessor.format_date_range(date_range)
    assert formatted == "01/2020 - Present"

def test_format_date():
    assert DataPreprocessor.format_date("2020") == "01/2020"
    assert DataPreprocessor.format_date("Present") == "Present"

def test_format_year():
    assert DataPreprocessor.format_year(2020) == "2020"
    assert DataPreprocessor.format_year("2020") == "2020"

def test_suggest_quantification():
    responsibility = "Led a team of developers"
    suggestion = DataPreprocessor.suggest_quantification(responsibility)
    assert "Suggestion" in suggestion
    assert "Original" in suggestion

def test_quantify_achievements():
    responsibilities = ["Developed new features", "Increased user engagement by 30%"]
    quantified = DataPreprocessor.quantify_achievements(responsibilities)
    assert len(quantified) == 2
    assert all(isinstance(resp, str) for resp in quantified)
