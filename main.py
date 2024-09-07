import json
import sys
import os
from template_manager import TemplateManager
from data_preprocessor import DataPreprocessor
from template_selector import TemplateSelector

def main():
    if len(sys.argv) != 4:
        print("Usage: python main.py <input_json_file> <output_html_file> <template_name>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    template_name = sys.argv[3]
    
    try:
        with open(input_file, 'r') as f:
            raw_data = json.load(f)
        
        preprocessed_data = DataPreprocessor.preprocess(raw_data)
        
        template_selector = TemplateSelector()
        selected_template = template_selector.get_template(template_name)
        
        template_manager = TemplateManager()
        html_output = template_manager.render_template(selected_template, preprocessed_data)
        
        if html_output is None:
            print("Failed to generate resume HTML.")
            sys.exit(1)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_output)
        print(f"Resume HTML generated: {output_file}")
    
    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in input file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()