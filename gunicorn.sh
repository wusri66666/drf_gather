#!/bin/bash

gunicorn -c gunicorn.py drf_gather.wsgi:application

