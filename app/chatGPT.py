import openai
from dotenv import dotenv_values
from time import sleep
import json
import copy

listItem = {
            "type": "listItem",
            "content": [
              {
                "type": "paragraph",
                "content": [
                  {
                    "type": "text",
                    "text": "List Item 3"
                  }
                ]
              }
            ]
          }

def convertStringToListItem(str):
    item = copy.deepcopy(listItem)    
    item['content'][0]['content'][0]['text'] = str
    return item

def convertStrToBulletPoints(str):
    tasks = [convertStringToListItem(s.lstrip('0123456789.- ')) for s in str.split('\n') if s != '']
    return tasks

def calculateUsage(usage):
    cost_per_token = 0.002 / 1000
    total_tokens = usage['total_tokens']
    return cost_per_token * total_tokens

openai.api_key = dotenv_values('.env')['OPEN_API_KEY']

prompts = {
    'problem_statement': "Hello ChatGPT, you will now act as a business analyst, who's main responsibility is to understand the requirements for a web application when it's given to you. I will give you a requirement, which is in HTML format. I want you to parse it, and list me the problem statement that this requirement is trying to solve.",
    'user_story': "Hello ChatGPT, you will now act as a business analyst, who's main responsibility is to understand the requirements for a web application when it's given to you. I will give you a requirement, which is in HTML format. I want you to parse it, and list me the user story that the requirement below is trying to solve in one bullet point. Could you output just the user story, starting with the exact text \"As a PB/PBA/SB, I want to\"",
    'frontend': "Hello ChatGPT, you will now act as a business analyst, who's main responsibility is to understand the requirements for a web application when it's given to you. I will give you a requirement, which is in HTML format. I want you to parse it, and list me the FE tasks in three bullet points?",
    'backend': "Hello ChatGPT, you will now act as a business analyst, who's main responsibility is to understand the requirements for a web application when it's given to you. I will give you a requirement, which is in HTML format. I want you to parse it, and list me the BE tasks in three bullet points?",
    'qa': "Hello ChatGPT, you will now act as a business analyst, who's main responsibility is to understand the requirements for a web application when it's given to you. I will give you a requirement, which is in HTML format. I want you to parse it, and list me any additional QA testing requirements in three bullet points?"
}

prompt_template_indices = {
    'problem_statement': 1,
    'user_story': 2,
    'frontend': [5, 1],
    'backend': [5, 2],
    'qa': [7, 2]
}

def generate_jira_content(requirement):
    with open('../jira-template.json') as f:
        jira_template = json.load(f)

    for prompt_key, prompt in prompts.items():
        print('Getting info for {}...'.format(prompt_key))
        chatgpt_prompt = prompt + '\n' + requirement

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                { "role": "user", "content": chatgpt_prompt }
            ],
            temperature=0.25
        )

        message = response.choices[0]['message']['content']
        tasks = convertStrToBulletPoints(message)

        print('Total cost: ${:.7f}'.format(calculateUsage(response.usage)))

        indices = prompt_template_indices[prompt_key]
    
        if type(indices) is list:
            jira_template['content'][indices[0]]['content'][indices[1]]['content'][1]['content'] = tasks
        else:
            jira_template['content'][indices]['content'][0]['text'] = message


        sleep(1) 
    
    return jira_template

def generate_jira_content_1(requirement):
    prompt = prompts['qa']

    chatgpt_prompt = prompt + '\n' + requirement

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            { "role": "user", "content": chatgpt_prompt }
        ],
        temperature=0.25
    )

    message = response.choices[0]['message']['content']
    tasks = convertStrToBulletPoints(message)

    print('Total cost: ${:.7f}'.format(calculateUsage(response.usage)))

    with open('../jira-template.json') as f:
        jira_template = json.load(f)

    indices = prompt_template_indices['qa']
    
    if type(indices) is list:
        jira_template['content'][indices[0]]['content'][indices[1]]['content'][1]['content'] = tasks
    else:
        jira_template['content'][indices]['content'][0]['text'] = message

    return jira_template