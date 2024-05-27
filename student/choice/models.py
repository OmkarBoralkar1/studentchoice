

# Create your models here.
# models.py
from django.db import models
import os
from uuid import uuid4

def get_file_path(instance, filename):
    # Generate a unique filename using a UUID
    _, ext = os.path.splitext(filename)
    filename = f"{uuid4()}{ext}"
    return os.path.join('uploads/', filename)

class YourModel(models.Model):
    file = models.FileField(upload_to=get_file_path)
    start_row = models.IntegerField()
    end_row = models.IntegerField()
    start_column = models.IntegerField()
    end_column = models.IntegerField()
