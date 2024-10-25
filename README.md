# Culinary API
This application aims to provide a REST API for registering and searching culinary recipes, catering to both chefs and users looking for cooking inspiration. The API was developed using Django Rest Framework (DRF) and PostgreSQL as the database, ensuring robustness and scalability.

## Features
1. Chefs Management:

- Access information about registered chefs in the system at /users/chefs/.
- Register as a chef to create your own recipes or view public and shared recipes.
- Filter chefs by name or roles such as baker, chef, executive chef, other, pastry chef, and sous chef.


2. Recipe Management:

- View public recipes without the need for login, as well as recipes shared with the user if logged in, and their own private recipes.
- Chefs can register recipes, which can be public or shared with a list of users by specifying usernames at /recipes/recipes/.
- Filter recipes by preparation time, cooking time, recipe name, serving size, and specific chefs.



## Stack used

**Back-end:** [Python](https://www.python.org/), [Django](https://www.djangoproject.com/), 
[Django-Rest-Framework](https://www.django-rest-framework.org/)

**Database:** [PostgreSQL](https://www.postgresql.org/)

**Containerization:** [Docker](https://www.docker.com/), [Docker Compose](https://docs.docker.com/compose/)

**Documentation:** [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/), 
[Swagger](https://swagger.io/), [Redoc](https://redoc.ly/), [RapiDoc](https://rapidocweb.com/)


## Installation

1. Clone the repository by executing the following command:
```bash
git clone https://github.com/ViniciusMeireles/culinary_api.git
```
2. Navigate to the project directory:
```bash
cd culinary_api
```
3. Start the Docker containers:
```bash
sudo docker compose up --build
```


## Running Unit Tests

To run the unit tests for the project using Docker Compose, follow these steps:


1. Run the following command to execute the unit tests:
- This command will start a temporary container, set up the test environment, run the unit tests, 
and display the results in the terminal.
```bash
sudo docker compose run web python manage.py test
```

- You can also run the tests in an existing container by executing the following commands:
```bash
sudo docker exec -it culinary_api-web-1 /bin/bash
python manage.py test
```

## API Documentation 
[![documentation](https://img.shields.io/badge/Documentation-blue)](http://127.0.0.1:8000/api/schema/redoc/)
[![test](https://img.shields.io/badge/Test_API-blue)](http://127.0.0.1:8000/api/schema/swagger-ui/)

To explore the complete API documentation, please visit 
[http://127.0.0.1:8000](http://127.0.0.1:8000). 
This page provides details on endpoints, parameters, and allows you to interactively test various features 
offered by the API.

Make sure you have the server running locally to access the documentation.