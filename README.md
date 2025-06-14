# Automate the Boring Stuff — Django Project with Celery & Redis

This guide explains how to set up a Django project called **Automate the Boring Stuff** on **macOS**, **Ubuntu**, and **Windows**, including virtual environments, database migrations, and async CSV import/export using Celery and Redis.

---

## 🛠️ Prerequisites

- Python 3.8+
- Git (optional)
- Redis
- VS Code (as code editor)

---

## 📦 1. Install VS Code

Download and install from: [https://code.visualstudio.com/](https://code.visualstudio.com/)

---

## 📁 2. Create Project Folder & Virtual Environment

```bash
mkdir automate-the-boring-stuff
cd automate-the-boring-stuff

# Create virtual environment
python -m venv env

# Activate it
source env/bin/activate      # macOS/Linux
env\Scripts\activate         # Windows
```

---

## 🌐 3. Install Django

```bash
pip install django
```

---

## 🏱 4. Create and Migrate Models

After writing your models in `models.py`, run:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 📁 5. Import/Export CSV via Custom Commands

Create commands in:

```
your_app/
└── management/
    └── commands/
        ├── import_csv.py
        └── export_csv.py
```

Run with:

```bash
python manage.py import_csv
python manage.py export_csv
```

---

## 🐌 6. Problem: Importing Millions of Rows Takes ~6 Minutes

To handle large imports asynchronously and improve responsiveness, we use **Celery + Redis**.

---

## 🚀 7. Install Celery and Redis Python Packages

```bash
pip install celery redis
```

Create a `celery.py` in your project root (`automate_the_boring_stuff/celery.py`) with:

```python
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'automate_the_boring_stuff.settings')

app = Celery('automate_the_boring_stuff')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

In `__init__.py` of the project folder:

```python
from .celery import app as celery_app
__all__ = ['celery_app']
```

---

## 🍎 macOS: Redis Setup

```bash
brew instal
