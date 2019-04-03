from django import template

register = template.Library()

def trim_url_tail(url):
    return "/".join(url.split('/')[:-2])

register.filter('trim_url_tail', trim_url_tail)
