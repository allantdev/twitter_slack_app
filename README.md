# twitter_slack_app
Pizza Demos

# Setup on macOS
Install Homebrew

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

cd to the project directory

create your creds and variables in a .env file at the root

to setup the pipenv environment run:
pipenv install

to start the bot run:
pipenv run python main.py