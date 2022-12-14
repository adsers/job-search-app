# screenr.ai | Job search app using NLP
![license logo](https://img.shields.io/github/license/adsers/job-search-app)
![last commit](https://img.shields.io/github/last-commit/adsers/job-search-app)


Watch demo video for the project:

[![Watch the video](https://drive.google.com/u/0/uc?id=1jfC2B-wDUWDdOTZz8I4PSV0Qe_ZKVgWI&export=download)](https://youtu.be/2h69fCHPUIU)

### Website link: https://adsers.pythonanywhere.com
---
### Description:
This is a Flask based web application that uses natural language processing to return the most relevant job results from a database of job listings.

Technologies used:
- HTML
- CSS
- JavaScript
- SQL
- Python
    - Selenium
    - SpaCy
    - Flask

The directory contains 2 files and 3 folders:

- `app.py`
- `master.db`
- `./static/` folder
- `./templates/` folder
- `./uploads/` folder

The database: master.db is a SQLite database that has two main tables, one for users and one for jobs, if the user opts to store their resume with the system, their details are added to the users table. The jobs table has information regarding data analyst and data science jobs in Delhi NCR region collected from naukri.com using a bot made via selenium.

The users table contains email IDs, file names of resumes (if stored), a unique index assigned to each user and a can_contact column, where a value of 1 is supplied if the user can be contacted for future opportunities and 0 is the user cannot be contacted for future oppourtunites.

The Flask application uses SpaCy to extract keywords and match them with job descriptions in the master database. It contains various helper functions in the start of the file to extract words from resume and clean the contents and check whether the files uploaded by users are of acceptable formats or not.

All the files are temporarily stored in the `./uploads/` folder when the application is running and if the user opts to not store their information, their resume is deleted from the folder after running the NLP algorithm.

The website has 3 main pages:
1. Search
2. About
3. Insights

The search page is the main page where users can search for jobs by uploading their resume, it has an optional field to enter email ID and asks if the user wants the website to store their information or not.

Once the user clicks search, they are returned the results page which is an extension of the search page that is only returned in case of POST requests. The results page uses jinja syntax to render the job postings and all relevant information along with apply links to the jobs.

The about page contains information about the website and the creator and the insights page contains a word cloud about the skills required in the data analyst and data science jobs in the database.

Bootstrap has been used as the primary CSS framework, however a custom stylesheet has also been added in the static folder to improve the aesthetics of the website.

How to run the app:
1. Fork the repository to local machine
2. Install Python 3.10 and install all additional dependencies in `requirements.txt` using the command `pip install -r ./requirements.txt`.
3. Navigate to the project folder and run the command `flask run` and you should get a message on your terminal showing the port where flask is running the web app.
4. Go to a web browser and enter that port to access the web app!

ALTERNATIVELY
The website can also be accessed on https://adsers.pythonanywhere.com/
