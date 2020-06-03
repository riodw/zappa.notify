import os

# SECURITY WARNING: don't run with debug turned on in production!
if 'PROD' in os.environ:
	DEBUG = False
	RUNNING_ENVIRON = 'PROD'

	try:
		from .config_prod import *
	except ImportError:
		print('####Unable to import production settings file:')

	ALLOWED_HOSTS = [
		'localhost',
		'127.0.0.1',
		'notify.pathfinder.io',
		'notify.medtricslab.com',
	]

elif 'DEV' in os.environ:
	DEBUG = True
	RUNNING_ENVIRON = 'DEV'

	try:
		from .config_dev import *
	except ImportError:
		print('####Unable to import development settings file:')
	
	ALLOWED_HOSTS = [
		'localhost',
		'127.0.0.1',
		'd6cf2fru5g.execute-api.us-east-2.amazonaws.com',
		'notify.pathfinder.io',
		'notify.medtricslab.com',
	]

else:
	DEBUG = True
	RUNNING_ENVIRON = 'LOCAL'

	try:
		from .config_dev import *
	except ImportError:
		print('####Unable to import development settings file:')
	
	ALLOWED_HOSTS = ['localhost','127.0.0.1']

# Current terms of service version number
CURRENT_TOS_VERSION = 1

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = '9_@m5+dmrlq#@#=yqumdw%s&@5n$6uduz-o7_7ir&se)q4$pig'
SECRET_KEY = SECRET_SECRET

# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'rest_framework',
	'rest_framework.authtoken',
	'corsheaders',
	'notification',
]

MIDDLEWARE_CLASSES = [
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# SITES FOR CORS
CORS_ORIGIN_WHITELIST = (
    'medtricslab.com',
    'localhost:8000',
    '127.0.0.1:8000'
)

# SET CORS FOR ALL SITES
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'notify.urls'

# Custom context processor
def custom_values(request):
	return {
		'CURRENT_TOS_VERSION':CURRENT_TOS_VERSION,
		'RUNNING_ENVIRON':RUNNING_ENVIRON,
	}

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'templates')],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
				'notify.settings.custom_values'
			],
		},
	},
]

CORS_ORIGIN_WHITELIST = (
	'amazonaws.com',
	's3.us-east-2.amazonaws.com',
	'medtricslab.com'
	'*'
)

WSGI_APPLICATION = 'notify.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
if 'RDS_DB_NAME' in os.environ:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'NAME': os.environ['RDS_DB_NAME'],
			'USER': os.environ['RDS_USERNAME'],
			'PASSWORD': os.environ['RDS_PASSWORD'],
			'HOST': os.environ['RDS_HOSTNAME'],
			'PORT': os.environ['RDS_PORT'],
		}
	}
elif DEBUG == False:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'NAME': 'notifications',
			'USER': 'postgres',
			'PASSWORD': '',
			'HOST': 'localhost',
			'PORT': '5432',
		}
	}
else:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.sqlite3',
			'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
		}
	}

# 'ENGINE': 'django.db.backends.sqlite3',
# 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]

# From rules
AUTHENTICATION_BACKENDS = (
	'rules.permissions.ObjectPermissionBackend',
	'django.contrib.auth.backends.ModelBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True




REST_FRAMEWORK = {
	# Use Django's standard `django.contrib.auth` permissions,
	# or allow read-only access for unauthenticated users.
	'DEFAULT_PERMISSION_CLASSES': [
		'rest_framework.permissions.DjangoModelPermissions',
	],
	# Not sure if these are neccessary?
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'rest_framework.authentication.BasicAuthentication',
		'rest_framework.authentication.SessionAuthentication',
		'rest_framework.authentication.TokenAuthentication',
	),
	#'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
	#'PAGE_SIZE': 100
	'DEFAULT_PARSER_CLASSES': ( 
		'rest_framework.parsers.JSONParser', 
		'rest_framework.parsers.FormParser', 
		'rest_framework.parsers.MultiPartParser', 
	) 
}

LOGIN_URL = 'rest_framework:login'
LOGOUT_URL = 'rest_framework:logout'

INTERNAL_IPS = (
	'127.0.0.1',
)

#LOGIN_REDIRECT_URL = ('.../api/')

STATIC_URL = '/static/'