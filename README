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

## The purpose of this project
This project was created as part of a hackathon. This proof of concept was completed in ~4 hours and work hasn't been done on it since. 
This code can still be used if anyone wants to expand on this idea. 