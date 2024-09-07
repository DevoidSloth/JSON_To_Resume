# Resume Generator

This project is a flexible and customizable resume generator that converts JSON data into beautifully formatted HTML resumes using various templates. It's particularly optimized for students but can be used by professionals at any career stage.

## Features

- Convert JSON resume data to HTML
- Multiple resume templates to choose from
- Customizable styles
- Responsive design for various screen sizes
- Print-friendly output
- Student-focused options and templates

## Prerequisites

- Python 3.7+
- Jinja2 templating engine

## Installation

1. Clone the repository:
```
git clone https://github.com/DevoidSloth/JSON_To_Resume.git
cd JSON_To_Resume
```


2. Install the required dependencies:
```
pip install -r requirements.txt
```

## Usage

To generate a resume, use the following command:

```
python main.py <input_json_file> <output_html_file> <template_name>
```

For example:
```
python main.py sample_data/test_resume.json resume.html modern_resume
```

## Project Structure

- `main.py`: The main entry point of the application
- `template_manager.py`: Manages the rendering of templates
- `data_preprocessor.py`: Preprocesses the input JSON data
- `template_selector.py`: Selects the appropriate template based on user input
- `Templates/`: Contains HTML templates for different resume styles
- `static/css/`: Contains CSS files for styling the resumes
- `sample_data/`: Contains sample JSON resume data for testing

## Available Templates

1. Modern Resume
2. Creative Resume
3. Polka Dotted Resume
4. Code Leaf Resume
5. Hexagon Harmony Resume
6. Origami Unfold Resume

## Customization

To create a new template:

1. Add a new HTML file in the `Templates/` directory
2. Create corresponding CSS styles in `static/css/`
3. Update the `template_selector.py` file to include the new template option

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.