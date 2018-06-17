import requests
import json

REQUEST_STATUS = "status"
REQUEST_CONTENT = "content"
REQUEST_KEY = "key"

def retrieveHtmls(urls):
    headers = {'user-agent': 'stock-picker/0.0.1'}
    s = requests.Session()
    responses = []
    for key, val in urls.items():
        page = s.get(val, headers=headers)
        response = {}
        response[REQUEST_KEY] = key
        response[REQUEST_STATUS] = page.status_code
        response[REQUEST_CONTENT] = page.text
        responses.append(response)
    return responses

def readTextFile(path):
    with open(path, "r") as f:
        return f.read()
    return ""

def dumpToJsonFile(data, encoder, destFile):
    with open(destFile, "w", encoding="utf-8") as fp:
        json.dump(data, fp, cls=encoder)

    