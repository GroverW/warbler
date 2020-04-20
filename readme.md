# Warbler
Warbler is a Twitter clone built using Flask. 

Features that have been implemented:
1) Creating a user
2) Profile page
3) Editing profiles
4) Following other users
5) Blocking other users
6) Writing posts
7) Liking posts


## Libraries
- Bcrypt: used for encrypting passwords
- WTForms: used for form validation
- SQLAlchemy: an Object Relational Mapper

## Setup
1) "python3 -m venv venv" at the root directory to create a virtual environment
2) "source venv/bin/activate" to activate the virtual environment
3) "pip install -r requirements.txt" to install requirements
4) "createdb warbler" to create a new database
5) "python seed.py" to seed the database
6) "flask run" to start the server at http://localhost:5000/


## Testing

How to run the test files:

1) "createdb warbler-test" to create the test database
2) "python seed.py" to seed the database
3) "python3 -m unittest -v name_of_test_file" to run one test file. The test files start with "_test". The -v flag can also be 
excluded if you do not want to see the status of individual tests.
