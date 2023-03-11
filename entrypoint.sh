#!/usr/bin/env bash
sleep 5
gunicorn --bind 0.0.0.0:5000 'app:app' --reload --access-logfile -
