import os

from .settings import *  # noqa
from .settings import BASE_DIR

# Configure the domain name using the environment variable
# that Azure automatically creates for us.
ALLOWED_HOSTS = (
    [os.environ["WEBSITE_HOSTNAME"], ".azurewebsites.net"]
    if "WEBSITE_HOSTNAME" in os.environ
    else []
)
CSRF_TRUSTED_ORIGINS = (
    ["https://" + os.environ["WEBSITE_HOSTNAME"]]
    if "WEBSITE_HOSTNAME" in os.environ
    else []
)
DEBUG = False

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "whitenoise.runserver_nostatic",
    "compressor",
    "home",
    "books",
]

# WhiteNoise configuration
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Add whitenoise middleware after the security middleware
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

STATIC_ROOT = os.path.join(BASE_DIR, "./static/")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Configure Postgres database based on connection string of the libpq Keyword/Value form
# https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING
conn_str = os.environ["AZURE_POSTGRESQL_CONNECTIONSTRING"]
conn_str_params = {
    pair.split("=")[0]: pair.split("=")[1] for pair in conn_str.split(" ")
}
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "OPTIONS": {"sslmode": conn_str_params["sslmode"]},
        "NAME": conn_str_params["dbname"],
        "HOST": conn_str_params["host"],
        "USER": conn_str_params["user"],
        "PASSWORD": conn_str_params["password"],
        "PORT": conn_str_params["port"],
    },
}
