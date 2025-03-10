# django-chatbot
A simple ChatGPT-powered chatbot built with Django using the MVT architecture.  
- Engage in multiple conversations simultaneously, each isolated by tab.  
- Your conversation context remains intact as long as the tab stays open, even after refreshing.  
- Once a tab is closed, the conversation is archived.  
- All conversation history is securely stored in the database.

## Prerequisite
Your system should have installed ```Python version 3.12``` and ```virtualenv```.

## How to install and run the code
1. Create a virtual environment to isolate the dependencies by running below commands.
```
# macOS/Linux
# You may need to run `sudo apt-get install python3-venv` first on Debian-based OSs
python3 -m venv .venv
source .venv/bin/activate

# Windows
# You can also use `py -3 -m venv .venv`
python -m venv .venv
.\venv\Scripts\activate
```
2. Install the dependency by running below commands from the root directory
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
3. Run migrate to create database
```
python django_backend/manage.py migrate
```
4. Replace the OPENAI_API_KEY value in ```.env``` file in the root directory with your own OpenAI API key.  
5. Run the setup.sh from root directory to run the django app
```./setup.sh```
6. Open http://localhost:8000/ to test the application

## Future Enhancement
1. use Django + React to separate the concerns of frontend and backend
2. Implement Login feature to store conversation based on user id, so that user can track their own conversations
3. Implement Assistant and Thread feature with openai for each user, so that they can manage multiple conversations
4. Store OPENAI_API_KEY in Github Secrets for better security
