class TemplateSelector:
    def __init__(self):
        self.templates = {
            'modern': 'modern_resume',
            'classic': 'classic_resume',
            'creative': 'creative_resume',
            'hexagon': 'hexagon_harmony_resume',
            'origami': 'origami_unfold_resume',
            'code-leaf': 'code_leaf_resume',
            'polka': 'polka_dotted_resume',
            
            
            
            # Add more templates as needed
        }

    def get_template(self, template_name):
        return self.templates.get(template_name, 'modern_resume')

    def list_templates(self):
        return list(self.templates.keys())

# Example usage:
# selector = TemplateSelector()
# template_name = selector.get_template('modern')
# available_templates = selector.list_templates()