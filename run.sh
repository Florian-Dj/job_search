#!/bin/bash

if ! [ -e data.db ]
then
        touch data.db
        python3 manage.py migrate
        python3 manage.py createsuperuser
        python3 manage.py collectstatic
fi

source env/bin/activate && screen -dmS django-jobs python manage.py runserver  --insecure 0:8000
