from django.contrib.auth import authenticate, login
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.http import JsonResponse
from . import server


#camera = server.camera()

# Create your views here.
def index(request):
    return HttpResponse("I am Okay")
    '''
    if request.user.is_authenticated:
        #camera.listen_thread()
        #status = camera.status
        #return render(request, 'dashboard/index.html', {'status' : status})
        return render(request, 'dashboard/index.html')
    else:
        return HttpResponseRedirect('../login')
    '''

'''
def frame_gen():
    while True:
        with camera.condition:
             camera.condition.wait()
             frame = camera.frame
             yield (b'--FRAME\r\n' + b'Content-Type : image/mjpeg\r\n\r\n' + frame + b'\r\n')

def start_stream(request):
    streamresponse = StreamingHttpResponse(frame_gen())
    streamresponse.headers['Cache-Control'] = 'no-cache, private'
    streamresponse.headers['Pragma'] = 'no-cache'
    streamresponse.headers['Content-Type'] = 'multipart/x-mixed-replace; boundary=FRAME'
    return streamresponse


def statusUpdate(request):
    with camera.statusChange:
        camera.statusChange.wait()
        statusResponse = JsonResponse({'status': str(camera.status), 'camera_address':str(camera.cam_addr)})
        return statusResponse
        '''