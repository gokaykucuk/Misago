"""Misago's default Django Project settings."""

import os
import structlog

__all__ = [
    "INSTALLED_APPS",
    "INSTALLED_PLUGINS",
    "MISAGO_NOTIFICATIONS_RETRY_DELAY",
    "TEMPLATE_CONTEXT_PROCESSORS",
]

import os

INSTALLED_APPS = [
    # Misago overrides for Django core feature
    "misago",
    "misago.users",
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.postgres",
    "django.contrib.humanize",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party apps used by Misago
    "ariadne_django",
    "celery",
    # "debug_toolbar",
    "mptt",
    "rest_framework",
    "social_django",
    # Misago apps
    "misago.admin",
    "misago.acl",
    "misago.analytics",
    "misago.cache",
    "misago.core",
    "misago.conf",
    "misago.icons",
    "misago.themes",
    "misago.markup",
    "misago.legal",
    "misago.notifications",
    "misago.categories",
    "misago.threads",
    "misago.readtracker",
    "misago.search",
    "misago.oauth2",
    "misago.socialauth",
    "misago.graphql",
    "misago.faker",
    "misago.menus",
    "misago.plugins",
    "misago.apiv2",
]

INSTALLED_PLUGINS = []

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.template.context_processors.debug",
    "django.template.context_processors.i18n",
    "django.template.context_processors.media",
    "django.template.context_processors.request",
    "django.template.context_processors.static",
    "django.template.context_processors.tz",
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "misago.acl.context_processors.user_acl",
    "misago.conf.context_processors.conf",
    "misago.conf.context_processors.og_image",
    "misago.core.context_processors.misago_version",
    "misago.core.context_processors.request_path",
    "misago.core.context_processors.momentjs_locale",
    "misago.icons.context_processors.icons",
    "misago.search.context_processors.search_providers",
    "misago.themes.context_processors.theme",
    "misago.legal.context_processors.legal_links",
    "misago.menus.context_processors.menus",
    "misago.users.context_processors.user_links",
    "misago.core.context_processors.hooks",
    # Data preloaders
    "misago.conf.context_processors.preload_settings_json",
    "misago.core.context_processors.current_link",
    "misago.markup.context_processors.preload_api_url",
    "misago.threads.context_processors.preload_threads_urls",
    "misago.users.context_processors.preload_user_json",
    "misago.categories.context_processors.preload_categories_json",
    "misago.socialauth.context_processors.preload_socialauth_json",
    # Note: keep frontend_context processor last for previous processors
    # to be able to expose data UI app via request.frontend_context
    "misago.core.context_processors.frontend_context",
]

MISAGO_NOTIFICATIONS_RETRY_DELAY = 5  # Seconds

HONEYBADGER = {
  'API_KEY': 'hbp_SGZoskKcsyPhjhMJCUryiKhuAQdwol21pJnL'
}


# Define LOGLEVEL based on environment variable, default to INFO
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False, # Keep existing loggers (like Honeybadger's)
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler', # Logs to stderr/stdout
            'formatter': 'verbose', # Use a detailed formatter
        },
        # Optional: Add Honeybadger handler if not automatically configured elsewhere
        # 'honeybadger': {
        #     'level': 'ERROR', # Send errors and higher to Honeybadger
        #     'class': 'honeybadger.contrib.django.handlers.LoggingHandler',
        # },
        # Optional: File handler (make sure the container user can write to the log path)
        # 'file': {
        #     'level': 'INFO',
        #     'class': 'logging.FileHandler',
        #     'filename': '/path/inside/container/django.log', # Choose a writable path
        #     'formatter': 'verbose',
        # },
    },
    'loggers': {
        'django': {
            'handlers': ['console'], # Send Django's logs to console
            'level': LOGLEVEL,       # Log level INFO or higher
            'propagate': True,       # Allow logs to propagate to the root logger
        },
        'django.request': {
            'handlers': ['console'], # Specifically log request handling errors
            'level': 'ERROR',        # Only log ERROR+ for request issues (less verbose)
            'propagate': False,      # Don't send request errors to root logger if handled here
        },
        # Add your app's logger if you use logging within your apps
        'misago': {
            'handlers': ['console'],
            'level': LOGLEVEL,
            'propagate': True,
        },
        # Root logger - catches everything else
        '': {
             'handlers': ['console'], # Add 'honeybadger' here too if using the handler
             'level': LOGLEVEL,
        }
    },
}
