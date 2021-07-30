from dashboard.models import CameraGateway, Frame
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.http import JsonResponse
#from . import server

gateway = None
frame = None

def getobjects():
    gateway = CameraGateway.objects.get(name="gate1")
    frame = Frame.objects.get(name="frame1") 
    gateway.frame = frame

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        getobjects()
        gateway.listen_thread()
        status = gateway.status
        return render(request, 'dashboard/index.html', {'status' : status, 'address' : gateway.cam_addr})
    else:
        return HttpResponseRedirect('../login')

def frame_gen():
    while True:
        with gateway.condition:
             gateway.condition.wait()
             streamFrame = frame.content
             yield (b'--FRAME\r\n' + b'Content-Type : image/mjpeg\r\n\r\n' + streamFrame + b'\r\n')

def start_stream(request):
    streamresponse = StreamingHttpResponse(frame_gen())
    streamresponse.headers['Cache-Control'] = 'no-cache, private'
    streamresponse.headers['Pragma'] = 'no-cache'
    streamresponse.headers['Content-Type'] = 'multipart/x-mixed-replace; boundary=FRAME'
    return streamresponse

def statusUpdate(request):
    with gateway.statusChange:
        gateway.statusChange.wait()
        statusResponse = JsonResponse({'status': str(gateway.status), 'camera_address':str(gateway.cam_addr)})
        return statusResponse