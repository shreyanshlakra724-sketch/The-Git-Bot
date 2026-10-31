# Github Repository/User Tracker Discord Bot

An open-source discord bot for tracking information regarding GitHub repositories and users using url/username/repository name.
<img width="713" height="525" alt="image" src="https://github.com/user-attachments/assets/7069f2e9-c8fe-4490-a51d-5003a7bbccba" />



# Commands

!track --> Tracks the GitHub repositories, provides information about it github repository url needs to be give in the following format:
  !track <repository_url>

!search -->Searches for GitHub repositories, repository name needs to be provided in the following format:
  !search <repository_name>

!user --> Searches for the user profile, provides information about the user, GitHub profile url or username needs to be provided in the following format:
  !user <username/user_url>

!commits -->Provides list of 10 latest commits of a repository, repository url needs to be provided in the following format:
  !commits <repository_url>

!issues -->Provides the list of 10 latest issues of a repository, repository url needs to be provided in the folloowing format:
  !issues <repository_url>

!contributors -->Provides the list of top 25 contributors of a repository, repository url needs to be provided in the following format:
  !contributors <repository_url>

!language -->Provides the languages used in a repository, then percentage of language used in project is represented via a bar graph:
  !language <repository_url>

  -Made using Python(Discord.py library,matplotlib,os,aiohttp,io)
  
Demo URLS:
https://discord.com/oauth2/authorize?client_id=1563878649248358420&permissions=117760&integration_type=0&scope=bot
https://discord.gg/MQssTRJb2w
