# #!/usr/bin/env bash
# # exit on error
# set -o errexit

# pip install -r requirements.txt

# python manage.py collectstatic --no-input
# python manage.py migrate
# if [[ $CREATE_SUPERUSER ]];
# then
#   python manage.py createsuperuser --no-input --email "$DJANGO_SUPERUSER_EMAIL"
# fi

#!/usr/bin/env bash
# exit on error
set -o errexit

# Install requirements
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Make migrations if needed
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check if the superuser already exists
if ! python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists())" | grep -q 'True'; then
    # Create superuser if it doesn't exist
    python manage.py createsuperuser --no-input --email "$DJANGO_SUPERUSER_EMAIL"
fi