from django.db import models
#first import django files when admin panel makethenuser comes
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
#extra
from pdf2image import convert_from_path
from PIL import Image
import os
from django.conf import settings
# Create your models here.
class Tweet(models.Model):
 user=models.ForeignKey(User,on_delete=models.CASCADE)
#  text=models.TextField(max_length=400)
#  photo=models.ImageField(upload_to='photo/',blank=True,null=True)
#  name = models.CharField(max_length=255,default="enter name")
 document = models.FileField(upload_to='documents/', blank=True, null=True)
 preview_image = models.ImageField(upload_to='document_images/', blank=True, null=True)
 description = models.TextField(blank=True) 
 email = models.EmailField(max_length=255, blank=True, null=True)  # Email field
 contact_number = models.CharField(max_length=15, blank=True, null=True)  # Phone number field
 # Allow for optional descriptions
#  price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  
#  price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=False, default=10.0)
 price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=False, default=10)
 status = models.CharField(max_length=50, choices=[('Available', 'Available'), ('Sold', 'Sold'), ('Pending', 'Pending')], default='Available')
 created_at=models.DateTimeField(auto_now_add=True)
 updated_at=models.DateTimeField(auto_now=True)
 payment_id=models.CharField(max_length=100,null=True)
#  creates=models.DateTimeField(auto_now_add=True)
 
 #it help to modify through username 
 def ___str__(self):
     return f'{self.user.username} - {self.text[:10]}'
 
 #add extra
def clean(self):
        super().clean()
        if self.document:
            # Validate allowed file extensions for document upload (e.g., PDF, PPT)
            if not self.document.name.endswith(('.pdf', '.ppt', '.pptx')):
                raise ValidationError("Only PDF and PPT/PPTX files are allowed.")
        
        if self.image:
            # Validate allowed file extensions for image upload (JPEG, PNG)
            if not self.image.name.endswith(('.jpeg', '.jpg', '.png')):
                raise ValidationError("Only JPEG, JPG, and PNG images are allowed.")
        
        # Validate email format
        if self.email and not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValidationError("Invalid email format.")
        
        # Validate contact number format (assuming it's a standard format)
        if self.contact_number:
            if not re.match(r"^\+?1?\d{9,15}$", self.contact_number):
                raise ValidationError("Invalid phone number format. Ensure it's in the correct international format.")


# Method to generate preview image of the PDF and save it
def save(self, *args, **kwargs):
        # Save the document first
        super().save(*args, **kwargs)
        
        if self.document_file and self.preview_image is None:
            # Generate preview image from the first page of the PDF
            self.generate_preview_image()
            super().save(*args, **kwargs)  # Save again with the preview image

def generate_preview_image(self):
        """
        Generate a preview image from the first page of the uploaded PDF
        and save it as an ImageField in the document model.
        """
        if self.document_file.name.endswith('.pdf'):
            try:
                # Path to the uploaded PDF file
                pdf_path = os.path.join(settings.MEDIA_ROOT, self.document_file.name)
                
                # Generate the preview (first page) as an image
                images = convert_from_path(pdf_path, first_page=1, last_page=1)
                
                # Save the generated image
                preview_image_path = os.path.join(settings.MEDIA_ROOT, 'document_images', f'{self.pk}_preview.jpg')
                images[0].save(preview_image_path, 'JPEG')
                
                # Set the preview image field to the generated image
                self.preview_image = f'document_images/{self.pk}_preview.jpg'
            except Exception as e:
                raise ValidationError(f"Error generating PDF preview: {e}")            