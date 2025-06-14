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
![Screenshot 2025-06-14 141228](https://github.com/user-attachments/assets/d65455de-d1c8-44de-bfc5-a899f3794878)
![Screenshot 2025-06-14 141348](https://github.com/user-attachments/assets/3fc31465-2408-4475-81bd-37886ab51954)
![Screenshot 2025-06-14 141457](https://github.com/user-attachments/assets/5ce24876-3fef-4753-b8d7-842f6845c0d7)
```

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

Windows does **not** officially support Redis. Use **one of the following**:

### Option 1: WSL (Recommended)

Install [WSL](https://learn.microsoft.com/en-us/windows/wsl/install), then install Redis inside Ubuntu:

```bash
sudo apt update
sudo apt install redis
```

### Option 2: Docker

Install [Docker Desktop](https://www.docker.com/products/docker-desktop) and run:

```bash
docker run -d -p 6379:6379 redis
```

To test:

```bash
docker exec -it <container_id> redis-cli
127.0.0.1:6379> ping
PONG
```

---

## Start Celery Worker

```bash
celery -A automate_the_boring_stuff worker --loglevel=info --pool=solo   # Use 'solo' on Windows
```

- `--pool=solo` is required for Windows due to lack of `fork()`.
- On macOS/Linux, default is fine.

---

## Example Command Flow

```bash
python manage.py import_csv
# This triggers the task and Celery handles it in the background
```

---

## Project is Ready!

You now have:

- A Django app with async capabilities  
- CSV import/export custom commands  
- Background task processing using Celery  
- Redis setup tailored for your OS
