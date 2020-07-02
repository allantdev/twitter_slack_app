This was a demo made for a prospective employer. It was made as an engineering exercise.
There are probably better solutions to achieve the same goal.

# Prior to setup Instructions:
Create Twitter account
Gain Dev Access
Save API creds
Get Slack account
Activate Webhooks
Integrate Twitter Slack Connector. Dont watch a user

# twitter_slack_app


# Setup on macOS
Open Terminal

Install Homebrew from their site

Install pyenv: 
brew install pyenv

Install new python: 
pyenv install 3.8.3

Add Pyenv global: 
pyenv global 3.8.3

Add pyenv to path: 
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.zshrc

Install pipenv:
pip install -U pipenv

Create your Pizza Demos Folder

cd to the folder

create your creds and variables in a .env file at the root

to setup the pipenv environment run:
pipenv install

to start the bot run:
pipenv run python main.py

# Your credentials for your own twitter and slack connector

Make a file named .env and put your creds in it in the base folder

CLIENT_KEY = "Twitter Customer Key"
CLIENT_SECRET = "Twitter Customer Secret"
SLACK_URL = "Slack webhook url for your app"
TWITTER_USER = "Twitter User you would like to follow"
