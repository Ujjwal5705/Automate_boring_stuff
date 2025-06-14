from django.shortcuts import render,redirect
from .utils import get_all_custom_models
from uploads.models import Upload
from django.contrib import messages
from .tasks import import_command

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
        import_command.delay(file_path, model_name)
        
        # Show the message to the user
        messages.success(request, 'Your file is being imported. You will be notified once it is done.')

        return redirect('import_data')
    else:
        custom_models = get_all_custom_models()
        context = {
            "custom_models": custom_models,
        }
        return render(request, 'dataentry/importdata.html', context)