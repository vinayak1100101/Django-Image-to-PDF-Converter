from django.urls import path
from .views import upload_images

urlpatterns = [
    path('', upload_images, name='convert_to_pdf'),
]
