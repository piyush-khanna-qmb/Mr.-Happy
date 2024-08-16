from urllib.parse import urlencode, urlsplit, urlunsplit

def create_content_url(content):
    query_string = urlencode({'content': content})

    return "?" + query_string

