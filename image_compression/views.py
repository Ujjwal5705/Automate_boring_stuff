from django.shortcuts import render
from .forms import CompressImageForm
from PIL import Image
from django.http import HttpResponse
import io


def compress(request):
    if request.method == 'POST':
        form = CompressImageForm(request.POST, request.FILES)
        if form.is_valid():
            original_img = form.cleaned_data['original_img']
            quality = form.cleaned_data['quality']
            compressed_image = form.save(commit=False)
            compressed_image.user = request.user

            # Perform Compression
            img = Image.open(original_img)
            img = img.convert('RGB')
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=quality, optimize=True)
            buffer.seek(0)

            # Saving the compressed image
            compressed_image.compressed_img.save(f'compressed_{original_img}', buffer)

            # Auto-download the compressed image
            response = HttpResponse(buffer.getvalue(), content_type='image/jpeg')
            response['Content-Disposition'] = f'attachment; filename=compressed_{original_img}'
            return response
    else:
        form = CompressImageForm()
        context = {
            'form': form,
        }
        return render(request, 'image_compression/compress.html', context)