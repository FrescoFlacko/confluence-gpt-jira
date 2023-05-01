from confluence import getRequirements
from chatGPT import generate_jira_content, generate_jira_content_1
from jira import createJira
import copy

pageId = "164038"

print('We will be generating requirements from your\'s Confluence page with id' + pageId)
print('Getting info from {}...'.format(pageId))

requirements = getRequirements(pageId)

print('Retrieved info from "{}"!'.format(requirements['title']))
print('Generating JIRA task info from OpenAI API...')

jira_template = generate_jira_content(requirements['description'])

print('Created description for user story!')

print('Uploading user story to JIRA...')

jira_id = createJira(pageId, jira_template, requirements['title'])

if jira_id != False:
    print('JIRA ticket created! {}'.format(jira_id))