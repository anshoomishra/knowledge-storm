from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    value = dictionary.get(key)
    print(f"Dictionary: {dictionary}, Key: {key}, Value: {value}")
    return value
