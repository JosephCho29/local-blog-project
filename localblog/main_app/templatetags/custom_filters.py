from django import template

register = template.Library()

@register.filter(name='truncate_words')
def truncate_words(value, num_words):
    words = value.split()[:num_words]
    return ' '.join(words) + '...' if len(value.split()) > num_words else value
