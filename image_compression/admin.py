from django.contrib import admin
from .models import CompressImage
from django.utils.html import format_html

# Register your models here.

class CompressImageAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        return format_html(f'<img src="{obj.compressed_img.url}" width="40" height="40" style="border-radius: 50%;">')
    
    def org_img_size(self, obj):
        img_size = obj.original_img.file.size
        if img_size < 1024:
            return f'{img_size} B'
        elif img_size < 1024*1024:
            return f'{round(img_size/1024, 2)} KB'
        else:
            return f'{round(img_size/(1024*1024), 2)} MB'
    
    def comp_img_size(self, obj):
        img_size = obj.compressed_img.file.size
        if img_size < 1024:
            return f'{img_size} B'
        elif img_size < 1024*1024:
            return f'{round(img_size/1024, 2)} KB'
        else:
            return f'{round(img_size/(1024*1024), 2)} MB'
    
    list_display = ['user', 'thumbnail', 'org_img_size', 'comp_img_size', 'compressed_at']


admin.site.register(CompressImage, CompressImageAdmin)