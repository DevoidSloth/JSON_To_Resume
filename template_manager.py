import jinja2
import os

class TemplateManager:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(current_dir, 'Templates')  # Note the capital 'T'
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir),
            autoescape=jinja2.select_autoescape(['html', 'xml'])
        )
        self.icons = {
            'email': 'PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJmZWF0aGVyIGZlYXRoZXItbWFpbCI+PHBhdGggZD0iTTQgNGgxNmMxLjEgMCAyIC45IDIgMnYxMmMwIDEuMS0uOSAyLTIgMkg0Yy0xLjEgMC0yLS45LTItMlY2YzAtMS4xLjktMiAyLTJ6Ij48L3BhdGg+PHBvbHlsaW5lIHBvaW50cz0iMjIsNiAxMiwxMyAyLDYiPjwvcG9seWxpbmU+PC9zdmc+',
            'phone': 'PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJmZWF0aGVyIGZlYXRoZXItcGhvbmUiPjxwYXRoIGQ9Ik0yMiAxNi45MnYzYTIgMiAwIDAgMS0yLjE4IDIgMTkuNzkgMTkuNzkgMCAwIDEtOC42My0zLjA3IDE5LjUgMTkuNSAwIDAgMS02LTYgMTkuNzkgMTkuNzkgMCAwIDEtMy4wNy04LjY3QTIgMiAwIDAgMSA0LjExIDJoM2EyIDIgMCAwIDEgMiAxLjcyIDEzLjgzIDE1LjgzIDAgMCAwIDEuMSAzLjMzIDIgMiAwIDAgMS0uNDUgMi4xMUw4LjA5IDkuOTFhMTYuODUgMTYuODUgMCAwIDAgNiA2bDEuMjctMS4yN2EyIDIgMCAwIDEgMi4xMS0uNDUgMTYuOTQgMTYuOTQgMCAwIDAgMy4zMSAxLjFBMiAyIDAgMCAxIDIyIDE2LjkyeiI+PC9wYXRoPjwvc3ZnPg==',
            'address': 'PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJmZWF0aGVyIGZlYXRoZXItbWFwLXBpbiI+PHBhdGggZD0iTTIxIDEwYzAgNy05IDEzLTkgMTNzLTktNi05LTEzYTkgOSAwIDAgMSAxOCAweiI+PC9wYXRoPjxjaXJjbGUgY3g9IjEyIiBjeT0iMTAiIHI9IjMiPjwvY2lyY2xlPjwvc3ZnPg=='
        }

    def render_template(self, template_name, data):
        try:
            template = self.env.get_template(f"{template_name}.html")
            data['icons'] = self.icons
            return template.render(data)
        except jinja2.exceptions.TemplateNotFound:
            print(f"Template not found: {template_name}.html")
            print(f"Current template directory: {self.env.loader.searchpath}")
            return None
        except Exception as e:
            print(f"An error occurred while rendering the template: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return None