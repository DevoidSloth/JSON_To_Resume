import json
import sys
import os
from typing import Tuple, Dict, Any
from template_manager import TemplateManager
from data_preprocessor import DataPreprocessor
from template_selector import TemplateSelector

def interactive_mode() -> Tuple[str, str, str]:
    print("Welcome to the interactive JSON to Resume converter!")
    
    # Get input JSON file
    while True:
        input_file = input("Enter the path to your input JSON file: ")
        if os.path.isfile(input_file):
            break
        print("File not found. Please try again.")
    
    # Get output HTML file
    while True:
        output_file = input("Enter the path for the output HTML file: ")
        if os.path.isdir(output_file):
            print("Please specify a file name, not just a directory.")
        elif os.path.splitext(output_file)[1].lower() != '.html':
            print("Please specify a file with a .html extension.")
        else:
            break
    
    # Get available templates
    template_selector = TemplateSelector()
    available_templates = template_selector.get_available_templates()
    
    # Display available templates
    print("\nAvailable templates:")
    for i, template in enumerate(available_templates, 1):
        print(f"{i}. {template}")
    
    # Select template
    while True:
        try:
            choice = int(input("\nEnter the number of the template you want to use: "))
            if 1 <= choice <= len(available_templates):
                template_name = available_templates[choice - 1]
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    return input_file, output_file, template_name

def main() -> None:
    if len(sys.argv) == 2 and sys.argv[1] == "--interactive":
        input_file, output_file, template_name = interactive_mode()
    elif len(sys.argv) == 4:
        input_file, output_file, template_name = sys.argv[1:]
    else:
        print("Usage: python main.py <input_json_file> <output_html_file> <template_name>")
        print("   or: python main.py --interactive")
        sys.exit(1)
    
    try:
        with open(input_file, 'r') as f:
            raw_data: Dict[str, Any] = json.load(f)
        
        preprocessed_data = DataPreprocessor.preprocess(raw_data)
        
        template_selector = TemplateSelector()
        selected_template = template_selector.get_template(template_name)
        
        if selected_template is None:
            print(f"Error: Invalid template name '{template_name}'. Available templates are: {', '.join(template_selector.list_templates())}")
            sys.exit(1)
        
        template_manager = TemplateManager()
        html_output = template_manager.render_template(selected_template, preprocessed_data)
        
        if html_output is None:
            print("Error: Failed to generate resume HTML. Please check your input data and template.")
            sys.exit(1)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_output)
        print(f"Resume HTML generated successfully: {output_file}")
    
    except FileNotFoundError as e:
        print(f"Error: File not found: {e.filename}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file: {e}")
        sys.exit(1)
    except KeyError as e:
        print(f"Error: Missing required key in input data: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        import traceback
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()