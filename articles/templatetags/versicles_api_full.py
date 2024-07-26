from django import template
from django.utils.safestring import mark_safe
import requests

register = template.Library()

@register.simple_tag
def fetch_versicle(article_reference):
    # Sua lógica para buscar o versículo baseado na referência
    # Por exemplo, chamar uma API ou uma função que retorna o texto do versículo

    api_url = f'https://bible-api.com/{article_reference}?translation=almeida'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        verse_text = data['text']
        # Limita o texto ao número máximo de caracteres

        verse_text = f'<em>"{verse_text}"</em>'
    else:
        verse_text = '<em>"Versículo não encontrado"</em>'

    return mark_safe(verse_text)
