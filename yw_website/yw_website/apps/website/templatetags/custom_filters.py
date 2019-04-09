from django import template

register = template.Library()

def trim_url_tail(url):
    return "/".join(url.split("/")[:-2])

def trailing_block_name(name):
    return name.split(".")[-1]

register.filter("trim_url_tail", trim_url_tail)
register.filter("trailing_block_name", trailing_block_name)
