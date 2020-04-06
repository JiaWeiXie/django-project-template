import os
import logging

from django.contrib.auth import get_user_model

User = get_user_model()
email = os.getenv('ADMIN_USERNAME')
password = os.getenv('ADMIN_PASSWORD')

if not User.objects.filter(email=email).exists():
    if email and password:
        User.objects.create_superuser(
            email,
            password
        )
        logging.info('Create admin success.')
    else:
        logging.warning("Can't found [ADMIN_USERNAME] or [ADMIN_PASSWORD].")
else:
    logging.warning('Admin user is exists.')