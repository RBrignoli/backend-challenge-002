# Backend Challenge #2 - The New Life Challenge

## Description

In this challenge you will develop a simplified version of The New Life app backend. You're expected to get all model's specifications from the design screens, while practicing the concepts learned in the first challenge.

### Entities

As mentioned in the description, the entities's structure must be exctracted from the [design screens](https://app.zeplin.io/project/5c670ec2dd0ba39a1b11af22) and respect the following user stories/requirements:

* 

### URLs    

The URL creation is at your own discretion, making use of nested routers.
If you have any doubts on how to implement these structures, check the
[Nested Routers documentation](https://github.com/alanjds/drf-nested-routers) and the [lookup field section on the Routers documentation](https://www.django-rest-framework.org/api-guide/routers/#simplerouter).

## Prerequisites
- [Python 3.7](https://www.python.org)
- [Docker](https://www.docker.com)
- [Docker Compose](https://docs.docker.com/compose/)
- [Virtualenv](https://github.com/pypa/virtualenv/)
- [Git](https://git-scm.com/)

## Instructions to Run

- Create the virtual environment and activate it

        virtualenv -p python3 venv
        source venv/bin/activate
- Install the requirements `pip install -r requirements.txt`
- Start the dockers `docker-compose up` with the database and the localstack
- Run the server with `python manage.py runserver 8000`

You need a `.env`file with your environment variables, here's an example file:
```
LOAD_ENVS_FROM_FILE='True'
ENVIRONMENT='development'
SECRET_KEY='#*=backend-challenge=*#'
DEFAULT_FROM_EMAIL='Challenge <challenge@jungledevs.com>'
DATABASE_URL='postgres://postgres:postgres@localhost:5432/boilerplate'
SENTRY_DSN='sentry_key'
AWS_STORAGE_BUCKET_NAME='django-be'
```

## Additional Information
Here are some useful stuff to keep in mind while completing this challenge:

* Try to keep your code [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself), so the creation of 
[abstract helper models](https://godjango.com/blog/django-abstract-base-class-model-inheritance/) is more than welcome to avoid repetition of fields in your models
* For better structuring and visualization, you may use 
[Nested Serializers](https://www.django-rest-framework.org/api-guide/relations/#nested-relationships) to customize your responses beyond the primary keys
