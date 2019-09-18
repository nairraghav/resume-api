# resume-service
This repository contains code for a resume service that will be used to create and resumes. The goal of this repository
is to learn how to use Flask, SQLAlchemy, and some other tools to kickstand a quick service to create users and experiences
to eventually create a resume. 


## API Endpoints

### Users
* [GET]  /api/users
* [GET]  /api/user/<user_id>
* [GET]  /api/user/search?email=<user_email>
* [GET]  /api/user/<user_id>/experiences
* [POST] /api/user/create
* [PUT]  /api/user/<user_id>

### Experiences
* [GET]  /api/experiences
* [GET]  /api/experience/<experience_id>
* [POST] /api/experience/create


## Upcoming Features

### Endpoints
* [PUT]    /api/experience/<experience_id>
* [DELETE] /api/user/<user_id>
* [DELETE] /api/experience/<experience_id>

### Front End
* Front-End to interact with API
* Templatize Resume
* Export To PDF