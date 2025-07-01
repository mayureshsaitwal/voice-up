#!/bin/sh

echo "Make Migrations...."
python manage.py makemigrations

echo "Running Migrations...."
python manage.py migrate

echo "Adding Mock Up Conversations...."
python manage.py load_mock_conversations

# echo "Starting Server...."
# python manage.py runserver 0.0.0.0:8000
