## What is this project
This is a project to take business requirements from Confluence and use GPT-3 to convert the requirements to JIRA tickets for developers to work on.

## How is this done?
This is done by the following flow:

 - Pulls the contents of a page from Confluence
 - Using pre-defined prompts, we ask GPT-3 to generate the following information for us:
	 - Problem Statement
	 - User Story (as a XXX)
	 - Frontend tasks
	 - Backend tasks
	 - QA testing tasks
 - We place the generated information into a JIRA template generated using the [Atlassian ADF Builder](https://developer.atlassian.com/cloud/jira/platform/apis/document/playground/).
 - We create a JIRA ticket using the JIRA API.
 - We link the Confluence page to the JIRA ticket so developers can go back to requirements and vice versa.

## The purpose of this project
This project was created as part of a hackathon. This proof of concept was completed in ~4 hours and work hasn't been done on it since. 
This code can still be used if anyone wants to expand on this idea. 

## Architecture
![Project Architecture]('images/cgj_architecture.png')
## Limitations
There are several notable limitations considering the project was developed in a few hours:
 - The flow is limited to 1 JIRA ticket per Confluence page.
 - There is currently a bug where the Confluence page is added via the [Remote Link API](https://developer.atlassian.com/server/jira/platform/jira-rest-api-for-remote-issue-links/) but the link doesn't display in JIRA.
 - The Confluence page ID is hardcoded, so code will need to be added to make it variable.
