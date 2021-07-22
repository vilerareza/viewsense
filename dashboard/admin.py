from django.contrib import admin
from .models import CameraGateway
from .models import Camera
from .models import Frame

# Register your models here.
admin.site.register(CameraGateway)
admin.site.register(Camera)
admin.site.register(Frame)
