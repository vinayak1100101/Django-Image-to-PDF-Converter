from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.conf import settings
from PIL import Image
from fpdf import FPDF
import os

def upload_images(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        image_paths = []

        for image in images:
            # Save the uploaded image and get the absolute file path
            path = default_storage.save(f'media/{image.name}', image)
            full_path = os.path.join(settings.MEDIA_ROOT, path)
            image_paths.append(full_path)
            print(f"Image saved at: {full_path}")  # Debugging line

        pdf = FPDF()
        for image_path in image_paths:
            if os.path.exists(image_path):
                image = Image.open(image_path)
                pdf.add_page()
                pdf.image(image_path, x=10, y=10, w=pdf.w - 20)
            else:
                print(f"File not found: {image_path}")  # Debugging line

        pdf_path = os.path.join(settings.MEDIA_ROOT, 'converted.pdf')
        pdf.output(pdf_path)

        # Serve the PDF as a download
        if os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="converted.pdf"'
                return response
        else:
            return HttpResponse("PDF generation failed.", status=500)

    return render(request, 'upload.html')
