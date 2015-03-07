#! /bin/bash

python ./public/staticServer.py &
PID="$!"
python manage.py runserver
kill -9 $PID 
