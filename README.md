# Resume App
[![Build Status](https://travis-ci.org/nairraghav/resume-app.svg?branch=master)](https://travis-ci.org/nairraghav/resume-app)

This repository contains code for a resume app that will be used to create resumes. The goal of this repository is to 
learn how to use Flask, SQLAlchemy, and some other tools to kickstand a quick service to create users and experiences
to eventually create a resume. 


## API Endpoints

### Users
* [GET]  /api/users
* [GET]  /api/user/<user_id>
* [GET]  /api/user/search?email=<user_email>
* [GET]  /api/user/<user_id>/experiences
* [POST] /api/user/create
* [PUT]  /api/user/<user_id>
* [DELETE] /api/user/<user_id>

### Experiences
* [GET]  /api/experiences
* [GET]  /api/experience/<experience_id>
* [POST] /api/experience/create
* [PUT]    /api/experience/<experience_id>
* [DELETE] /api/experience/<experience_id>


## How To Run

### Install Requirements
```bash
pip install -r requirements.txt
```

### Export Flask App
```bash
export FLASK_APP=src/app.py
```

### Initialize / Seed DB
```bash
flask init_db
flask seed_db
```

### Run Flask
```bash
flask run
```

## Hosted At
This API is currently hosted [here](resume-api.raghav-nair.com) via Heroku & Google Domains. CI handled using Travis-CI
