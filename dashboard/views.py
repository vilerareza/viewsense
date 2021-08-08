from dashboard.models import CameraGateway, Frame
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.http import JsonResponse
from . import server_

gateway = None
frame = None
#gateway = CameraGateway.objects.get(name="gate1")
#frame = Frame.objects.get(name="frame1")
#gateway.frame = frame

#gateway = server_.camera()

def getobjects():
    global gateway
    global frame	    
    gateway = CameraGateway.objects.get(name="gate1")
    frame = Frame.objects.get(name="frame1") 
    gateway.frame = frame

# Create your views here.
def index(request):
    global gateway
    if request.user.is_authenticated:
        if ((gateway is None) & (frame is None)):
            getobjects()
        gateway.listen_thread()
        print('gateway listen')
        status = gateway.status
        return render(request, 'dashboard/index.html', {'status' : status, 'address' : gateway.cam_addr})
    else:
        return HttpResponseRedirect('../login')

def frame_gen():
    global gateway
    global frame
    print('iterrating frame')
    while True:
        with gateway.condition:
             gateway.condition.wait()
             #yield (b'--FRAME\r\n' + b'Content-Type : image/mjpeg\r\n\r\n' + gateway.frame + b'\r\n')
             streamFrame = frame.content
             yield (b'--FRAME\r\n' + b'Content-Type : image/mjpeg\r\n\r\n' + streamFrame + b'\r\n')

def start_stream(request):
    print('stream.mjpg received from client - start StreamingHTTPResponse')
    streamresponse = StreamingHttpResponse(frame_gen())
    streamresponse.headers['Cache-Control'] = 'no-cache, private'
    streamresponse.headers['Pragma'] = 'no-cache'
    streamresponse.headers['Content-Type'] = 'multipart/x-mixed-replace; boundary=FRAME'
    return streamresponse

def statusUpdate(request):
    global gateway
   
    with gateway.statusChange:
        print('client requesting status update')
        gateway.statusChange.wait()
        statusResponse = JsonResponse({'status': str(gateway.status), 'camera_address':str(gateway.cam_addr)})
        print('status updated to client')
        return statusResponse
