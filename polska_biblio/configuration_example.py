# This file is just an configuration example, do not use it like it is.
# It should be copied, filled and renamed to 'configuration.py'.

#########################
#                       #
#   Required settings   #
#                       #
#########################

# This is a list of valid fully-qualified domain names (FQDNs) for the Django server. The first FQDN in the list will be treated as the preferred name.
#
# Example: ALLOWED_HOSTS = ['localhost', '127.0.0.1']
ALLOWED_HOSTS = []

# PostgreSQL database configuration.
DATABASE = {
    'NAME': '',         # Database name
    'USER': '',               # PostgreSQL username
    'PASSWORD': '',           # PostgreSQL password
    'HOST': 'localhost',      # Database server
    'PORT': '',               # Database port (leave blank for default)
    'CONN_MAX_AGE': 300,      # Max database connection age
}

# This key is used for secure generation of random numbers and strings. It must never be exposed outside of this file.
# For optimal security, SECRET_KEY should be at least 50 characters in length and contain a mix of letters, numbers, and
# symbols. The Django server won't run without this defined. For more information, see
# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-SECRET_KEY
SECRET_KEY = ''


#########################
#                       #
#   Optional settings   #
#                       #
#########################

# Specify one or more name and email address tuples representing Django server administrators. These people will be notified of
# application errors (assuming correct email settings are provided).
ADMINS = [
    # ['John Doe', 'jdoe@example.com'],
]
