from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parents[2]
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(BASE_DIR.parent / '.env')
SECRET_KEY = env('SECRET_KEY', default='unsafe-development-key-change-me')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])
INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
    'crispy_forms', 'crispy_bootstrap5', 'ckeditor', 'ckeditor_uploader',
    'corsheaders', 'rest_framework',
    'apps.accounts', 'apps.core', 'apps.blog', 'apps.events', 'apps.faculty',
    'apps.gallery', 'apps.contact', 'apps.news',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware', 'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'apps.accounts.middleware.AutoLogoutMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'config.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [BASE_DIR / 'templates'], 'APP_DIRS': True,
              'OPTIONS': {'context_processors': ['django.template.context_processors.debug', 'django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION = 'config.wsgi.application'
DATABASE_URL = env('DATABASE_URL', default=env('POSTGRES_URL', default=''))
DATABASES = {'default': env.db('DATABASE_URL', default=DATABASE_URL or 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
    user=env('DB_USER', default='cseblog_user'),
    password=env('DB_PASSWORD', default='cseblog_password'),
    host=env('DB_HOST', default='localhost'),
    port=env('DB_PORT', default='5432'),
    name=env('DB_NAME', default='cseblog_db'),
))}
AUTH_USER_MODEL = 'accounts.AdminUser'
LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_TZ = 'en-us', 'Asia/Kolkata', True, True
STATIC_URL, STATIC_ROOT = '/static/', env('STATIC_ROOT', default=str(BASE_DIR / 'staticfiles'))
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL, MEDIA_ROOT = '/media/', env('MEDIA_ROOT', default=str(BASE_DIR / 'media'))
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'
CKEDITOR_UPLOAD_PATH = 'ckeditor/'
CKEDITOR_CONFIGS = {'default': {'toolbar': 'Custom', 'toolbar_Custom': [['Bold','Italic','Underline','Strike'], ['NumberedList','BulletedList'], ['Link','Unlink'], ['Image','Table','CodeSnippet'], ['Format','FontSize'], ['RemoveFormat','Source']], 'height': 400, 'extraPlugins': 'codesnippet'}}
SESSION_COOKIE_AGE = 28800
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER, SECURE_CONTENT_TYPE_NOSNIFF, X_FRAME_OPTIONS = True, True, 'DENY'
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS = env('EMAIL_HOST', default=''), env.int('EMAIL_PORT', default=587), env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER, EMAIL_HOST_PASSWORD = env('EMAIL_HOST_USER', default=''), env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL, CONTACT_NOTIFY_EMAIL = env('DEFAULT_FROM_EMAIL', default='CSE Blog <cse@example.com>'), env('CONTACT_NOTIFY_EMAIL', default='hod@example.com')
CELERY_BROKER_URL = env('REDIS_URL', default='redis://localhost:6379/0')
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', 'LOCATION': 'cseblog'}}
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
