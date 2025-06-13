from django.apps import apps

def get_all_custom_models():
    default_models = ['LogEntry', 'Permission', 'Group', 'User', 'ContentType', 'Session', 'Upload']
    Custom_models = []
    for model in apps.get_models():
        if model.__name__ not in default_models:
            Custom_models.append(model.__name__)
    return Custom_models
    