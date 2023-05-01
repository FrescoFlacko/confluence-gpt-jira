import requests
from requests.auth import HTTPBasicAuth
from dotenv import dotenv_values
import json

main_domain = dotenv_values('.env')['MAIN_DOMAIN']
username = dotenv_values('.env')['ATLASSIAN_EMAIL']

page_url = '{}/wiki/api/v2/pages'.format(main_domain)

auth = HTTPBasicAuth(username, dotenv_values('.env')['ATLASSIAN_API_KEY'])

headers = {
    'Accept': 'application/json'
}

def getRequirements(confluence_page_id):
    page_id = '/{}?body-format=storage'.format(confluence_page_id)

    response = requests.request(
        'GET',
        page_url + page_id,
        headers=headers,
        auth=auth
    )

    body = json.loads(response.text)

    return {
        'title': body['title'],
        'description': body['body']['storage']['value']
    }
