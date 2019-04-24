from django import template
from yw_website.apps.website.utils import truncate

register = template.Library()

def trim_url_tail(url):
    return "/".join(url.split("/")[:-2])

def trailing_block_name(name):
    return name.split(".")[-1]

def pretty_bytes(num_bytes):
    format_string = "{} {}"
    if num_bytes < 1000:
        unit = "B"
    elif num_bytes < 1000000:
        unit = "kB"
        num_bytes = num_bytes / 1000
    elif num_bytes < 1000000000:
        unit = "MB"
        num_bytes = num_bytes / 1000000
    elif num_bytes < 1000000000000:
        unit = "GB"
        num_bytes = num_bytes / 1000000000
    else:
        unit = "TB"
        num_bytes = num_bytes / 1000000000000
    return "{} {}".format(truncate(num_bytes, 3),  unit)

register.filter("trim_url_tail", trim_url_tail)
register.filter("trailing_block_name", trailing_block_name)
register.filter("pretty_bytes", pretty_bytes)
