#!/bin/bash

if ! [ -e data.db ]
then
        touch data.db
        python3 manage.py migrate
fi

source env/bin/activate && screen -dmS django-jobs python manage.py runserver 0:8000
