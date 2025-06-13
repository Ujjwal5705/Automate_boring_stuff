from django.shortcuts import render,redirect
from .utils import get_all_custom_models
from django.http import HttpResponse
from uploads.models import Upload
from django.conf import settings
from django.core.management import call_command
from django.contrib import messages

# Create your views here.

def import_data(request):
    if request.method == 'POST':
        file = request.FILES.get('file_path')
        model_name = request.POST.get('model_name')

        # Store this file in Upload model
        upload = Upload.objects.create(file=file, model_name=model_name)

        # file path
        file_path = str(upload.file.path)

        # Trigger importdata command
        try:
            call_command('importdata', file_path, model_name)
            messages.success(request, 'Data imported Successfully!')
        except Exception as e:
            messages.error(request, str(e))
        
        return redirect('import_data')
    else:
        custom_models = get_all_custom_models()
        context = {
            "custom_models": custom_models,
        }
        return render(request, 'dataentry/importdata.html', context)