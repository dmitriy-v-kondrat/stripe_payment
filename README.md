Test task:

https://docs.google.com/document/d/1RqJhk-pRDuAk4pH1uqbY9-8uwAqEXB9eRQWLSMM_9sI/edit?pli=1



Python 3.8.10

Django 4.2.7


Add the .env file to the project root and edit it.

    SECRET_KEY='your key'
    api_key= 'your key'
    STRIPE_WEBHOOK_SECRET= 'your key'
    STRIPE_PUBLIC_KEY= 'your key'
    RATE_API='https://www.exchangerate-api.com/'


Build project in a docker:

    docker-compose build


Run project:

    docker-compose up

If create admin:

    docker exec -it  stripe_payment python manage.py createsuperuser


The database is filled with instances Item, Tax, Discount when docker starts
