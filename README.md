# Inventory Management Lab

A simple inventory management system with a Flask API and CLI, integrated with OpenFoodFacts.

## Features
- List, add, view, update, and delete inventory items
- Fetch product details from OpenFoodFacts API
- CLI interface for easy interaction

## Requirements
- Python 3.12+  
- Flask  
- Requests  
- pytest (for unit testing)

## Setup
1. Clone the repo:
git clone <your-repo-url>
cd flask-lab-final

pipenv install
pipenv shell
# or
pip install -r requirements.txt


2. Run the server:
python server.py

3. Run the CLI:
python cli.py

4. Run the tests:
pytest tests/test.py