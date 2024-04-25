import base64
import urllib.parse

def b64_e(text):
    data_bytes = text.encode('ASCII')
    encoded_bytes = base64.b64encode(data_bytes)
    encoded_text = encoded_bytes.decode('ASCII')
    return encoded_text

def b64_d(text):
    return(base64.b64decode(text.encode('ASCII')).decode('ASCII'))

def url_e(text):
    return urllib.parse.quote(text)

def url_d(text):
    return urllib.parse.unquote(text)

    