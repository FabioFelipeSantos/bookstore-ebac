#!/bin/bash
git pull
python manage.py collectstatic --noinput
