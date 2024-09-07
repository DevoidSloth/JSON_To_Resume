from typing import Dict, List, Optional, Tuple

class TemplateSelector:
    def __init__(self):
        self.templates: Dict[str, Tuple[str, str]] = {
            'modern': ('modern_resume', 'A clean and professional design with a focus on readability'),
            'classic': ('classic_resume', 'A traditional layout suitable for conservative industries'),
            'creative': ('creative_resume', 'A unique design for showcasing creativity and personality'),
            'hexagon': ('hexagon_harmony_resume', 'A modern design featuring hexagonal elements for a balanced look'),
            'origami': ('origami_unfold_resume', 'An artistic design inspired by origami, perfect for creative fields'),
            'code-leaf': ('code_leaf_resume', 'A tech-inspired design with a nature twist, ideal for developers'),
            'polka': ('polka_dotted_resume', 'A playful design with polka dots, suitable for vibrant personalities'),
            'ats_friendly': ('ats_friendly_resume', 'A simple, clean design optimized for applicant tracking systems'),
        }

    def get_template(self, template_name: str) -> Optional[str]:
        return self.templates.get(template_name, (None, ''))[0]

    def list_templates(self) -> List[str]:
        return list(self.templates.keys())

    def get_available_templates(self) -> List[str]:
        return self.list_templates()

    def validate_template_name(self, template_name: str) -> bool:
        return template_name in self.templates

    def get_template_description(self, template_name: str) -> Optional[str]:
        return self.templates.get(template_name, (None, ''))[1]

    def get_templates_with_descriptions(self) -> List[Tuple[str, str]]:
        return [(name, description) for name, (_, description) in self.templates.items()]