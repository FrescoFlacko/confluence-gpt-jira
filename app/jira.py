import requests
from requests.auth import HTTPBasicAuth
from dotenv import dotenv_values
import json

main_domain = dotenv_values('.env')['MAIN_DOMAIN']
username = dotenv_values('.env')['ATLASSIAN_EMAIL']

issue_url = '{}/rest/api/3/issue'.format(main_domain)

auth = HTTPBasicAuth(username, dotenv_values('.env')['ATLASSIAN_API_KEY'])

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

def updateRemoteLink(ticket, pageId):
    get_issue_url = issue_url + '/' + ticket + '/remotelink'

    payload = json.dumps( {
        "application": {
            "name": "System Confluence",
            "type": "com.atlassian.confluence"
        },
        "id": 10000,
        "object": {
            "icon": {},
            "status": {
                "icon": {}
            },
            "title": "Wiki Page",
            "url": main_domain + "/wiki/pages/viewpage.action?pageId=" + pageId
        },
        "relationship": "Wiki Page",
    }
    )

    response = requests.request(
        'POST',
        get_issue_url,
        data=payload,
        headers=headers,
        auth=auth
    )

    print(json.dumps(json.loads(response.text), indent=4))
    return True if response.status_code == 200 else False

def createJira(pageId, description, summary):
    payload = json.dumps(
        {
        "fields": {
            "description": description,
            "issuetype": {
                "description": "Tasks track small, distinct pieces of work.",
                "entityId": "bfd6e18b-976a-45e9-8871-d112c0c1c73c",
                "iconUrl": main_domain + "/rest/api/2/universal_avatar/view/type/issuetype/avatar/10318?size=medium",
                "id": "10001",
                "name": "Task",
                "self": main_domain + "/rest/api/3/issuetype/10001",
                "subtask": False
            },
            "summary": summary,
            "project": {
                "avatarUrls": {
                    "16x16": main_domain + "/rest/api/3/universal_avatar/view/type/project/avatar/10417?size=xsmall",
                    "24x24": main_domain + "/rest/api/3/universal_avatar/view/type/project/avatar/10417?size=small",
                    "32x32": main_domain + "/rest/api/3/universal_avatar/view/type/project/avatar/10417?size=medium",
                    "48x48": main_domain + "/rest/api/3/universal_avatar/view/type/project/avatar/10417"
                },
                "id": "10000",
                "key": "TEST",
                "name": "Test",
                "self": main_domain + "/rest/api/3/project/10000",
                "simplified": False
            },
            "reporter": {
                "accountId": "712020:2df69a59-988f-4f61-a123-903da25e9bc3",
                "accountType": "atlassian",
                "active": True,
                "avatarUrls": {
                    "16x16": "https://secure.gravatar.com/avatar/989839e765adfad72002e95ad9e6bf24?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FYA-1.png",
                    "24x24": "https://secure.gravatar.com/avatar/989839e765adfad72002e95ad9e6bf24?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FYA-1.png",
                    "32x32": "https://secure.gravatar.com/avatar/989839e765adfad72002e95ad9e6bf24?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FYA-1.png",
                    "48x48": "https://secure.gravatar.com/avatar/989839e765adfad72002e95ad9e6bf24?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FYA-1.png"
                },
                "displayName": "Test",
                "emailAddress": username,
                "self": main_domain + "/rest/api/3/user?accountId=712020%3A2df69a59-988f-4f61-a123-903da25e9bc3",
                "timeZone": "America/Toronto"
            }
        },
        "update": {}
    }
    )

    print(payload)

    response = requests.request(
        'POST',
        issue_url,
        data=payload,
        headers=headers,
        auth=auth
    )
    
    body = json.loads(response.text)

    if response.status_code == 201:
        updateRemoteLink(body['key'], pageId)
        return body['key']
    else:
        print('This call failed!')
        print(body)
        return False
