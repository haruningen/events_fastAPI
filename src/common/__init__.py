from jinja2 import Environment, FileSystemLoader, select_autoescape

__all__ = ('templates_env',)

templates_env = Environment(
    loader=FileSystemLoader('./templates'),
    autoescape=select_autoescape()
)
