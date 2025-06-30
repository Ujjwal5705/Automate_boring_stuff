# Automate the Boring Stuff

This guide explains how to set up a Django project called **Automate the Boring Stuff** on **macOS**, **Ubuntu**, and **Windows**, including virtual environments, database migrations, and async CSV import/export using Celery and Redis.

---

## Prerequisites

- Python 3.8+
- Git (optional)
- Redis
- Celery
- VS Code (as code editor)

## 1. Install VS Code

Download and install from: [Link](https://code.visualstudio.com/download)

## 2. Create Project Folder & Virtual Environment

```bash
mkdir automate-the-boring-stuff
cd automate-the-boring-stuff

# Create virtual environment
python -m venv env

# Activate it
source env/bin/activate      # macOS/Linux
env\Scripts\activate         # Windows
```

## 3. Install Django in virtual Environment

```bash
pip install django
```

## 4. Create and Migrate Models

After writing your models in `models.py`, run below commands to sync the changes with the database:

```
python manage.py makemigrations
python manage.py migrate
```

## 5. Import/Export CSV via Custom Commands

Create commands in:

```
your_app/
└── management/
    └── commands/
        ├── importdata.py
        └── exportdata.py
```

Run with:

```bash
python manage.py importdata file_path model_name
python manage.py exportdata model_name
```

## 6. Problem: Importing Millions of Rows Takes ~7 Minutes

```
To handle large imports asynchronously and improve responsiveness, we use **Celery + Redis**.
```
[![Screenshot-2025-06-14-141228.png](https://i.postimg.cc/sg1gDPLC/Screenshot-2025-06-14-141228.png)](https://postimg.cc/dhPY5Cv5)
[![Screenshot-2025-06-14-141348.png](https://i.postimg.cc/DzXf1vFC/Screenshot-2025-06-14-141348.png)](https://postimg.cc/yJ7zHzD9)
[![Screenshot-2025-06-14-141422.png](https://i.postimg.cc/Mp4KcMkM/Screenshot-2025-06-14-141422.png)](https://postimg.cc/CRGVXKxS)

## 7. Install Celery and Redis Python Packages

```bash
pip install celery redis
```

Create a `celery.py` in your project root (`automate_the_boring_stuff/celery.py`) with:

```python
import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

app = Celery('proj')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
```

In `__init__.py` of the project folder:

```python
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)
```

---

## macOS: Redis Setup

```bash
brew install redis
redis-server
brew services start redis
```

To verify Redis is running:

```bash
brew services list
```

You should see:

```
redis (homebrew.mxcl.redis)
Running: ✔
```

Test with:

```bash
redis-cli
127.0.0.1:6379> ping
PONG
```

Stop Redis:

```bash
brew services stop redis
```

---

## Ubuntu (Linux): Redis Setup

```bash
sudo apt update
sudo apt install redis-tools    # for redis-cli
sudo snap install redis
```

Enable Redis on startup:

```bash
sudo snap set redis service.start=true
```

Start Redis server (if using `apt`):

```bash
sudo systemctl start redis
```

Stop server:

```bash
sudo systemctl stop redis
```

Test:

```bash
redis-cli
127.0.0.1:6379> ping
PONG
```

---

## Windows: Redis Setup

Windows does **not** officially support Redis. Use the following method. It worked for me :)

### WSL

Install [WSL](https://learn.microsoft.com/en-us/windows/wsl/install), then install Redis inside Ubuntu:

Open PowerShell or Windows Command Prompt in administrator mode by right-clicking and selecting "Run as administrator", enter the wsl --install command, then restart your machine.
After that use the following command for Redis setup
```bash
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
sudo apt-get update
sudo apt-get install redis
```

---

Lastly, start the Redis server like so:
```bash
sudo service redis-server start
```

Once Redis is running, you can test it by running redis-cli:
```bash
redis-cli
```
Test the connection with the ping command:
```bash
127.0.0.1:6379> ping
PONG
```

It would look like this :

---
[![Screenshot-2025-06-14-143759.png](https://i.postimg.cc/CLnfcgFq/Screenshot-2025-06-14-143759.png)](https://postimg.cc/JGmnhSHr)
[![Screenshot-2025-06-14-143814.png](https://i.postimg.cc/K8X3VHzs/Screenshot-2025-06-14-143814.png)](https://postimg.cc/N5402bR1)


## Start Celery Worker

Below command will work in macOS/Linux only
Celery uses prefork by default, which works only on Unix systems.
```bash
celery -A automate_the_boring_stuff worker --loglevel=info
```

On Windows, you need to explicitly use the solo pool (single-threaded, no multiprocessing)
- `--pool=solo` is required for Windows due to lack of `fork()`.
- solo uses a single thread and avoids these issues but is not suitable for production (only development/testing).
```bash
celery -A awd_main worker --loglevel=info --pool=solo
```

Note: Make sure you set the Celery broker url to localhost 6379 in settings.py and redis server is running in background
```bash
CELERY_BROKER_URL = 'redis://localhost:6379'
```

After all, your terminal should look like this:
---
[![Screenshot-2025-06-14-150322.png](https://i.postimg.cc/QCw0KZDr/Screenshot-2025-06-14-150322.png)](https://postimg.cc/m13QKqhd)

## Example Command Flow

```bash
python manage.py importdata file_path moel_name
# This triggers the task and Celery handles it in the background
```

---

## 📨 Email on Import Completion

After a CSV import completes, the user receives an email from the default sender email configured in `settings.py`.

### Step 1: Setup Email Configuration

In your `settings.py`, add the following and 

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```
If using Gmail, enable 2FA and use an App Password instead of your actual account password.


