from django.db import models

# Create your models here.

import io
import socket
import selectors
import threading
from threading import Condition

class CameraGateway (models.Model):

    # Model field
    name = models.CharField(max_length=30)

    # Attribute
    host = ''
    port = 65003
    status = 'No Camera Connection'
    cam_addr =''
    frameInitialized = False
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sel = selectors.DefaultSelector()
    condition = Condition()
    buffer = io.BytesIO()
    #frame = bytes()
    frame = None
    statusChange = Condition()
    t_listen = threading.Thread()
    

    # Model methods
    
    def __write(self, buf):   
    # frame and buffer writer 
        if buf.startswith(b'\xff\xd8'):
            self.buffer.truncate()
            with self.condition:
                #self.frame = self.buffer.getvalue()
                self.frame.content = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)

        return self.buffer.write(buf)
        
    def __accept_wrapper(self,sock):
    # accept new connections
        conn, addr = sock.accept()
        self.cam_addr = addr[0]
        print ('accepted connection from ', addr)
        conn.setblocking(False)
        events = selectors.EVENT_READ
        self.sel.register(conn,events, data = addr)

        with self.statusChange:
            self.status = 'Connected'
            self.statusChange.notify_all()


    def __service_connection (self, key, mask):
    # Receive data
        sock = key.fileobj
        data = key.data
        try: 
            camfile1 = sock.makefile('rb')
            if mask & selectors.EVENT_READ:
                #receiving data
                camData = camfile1.read()
                self.__write(camData)
                #check the camera connection
                sock.send(b'1')
        except:
            print ('closing connection to ', data)
            self.sel.unregister(sock)
            sock.close()
            with self.statusChange:
                self.status = 'No Camera Connection'
                self.statusChange.notify_all()
            self.frameInitialized = False


    def __listen(self):
    # Listen for new connection
        self.lsock.bind((self.host,self.port))
        self.lsock.listen()
        print('listening on, ', (self.host,self.port))
        self.lsock.setblocking(False)
        self.sel.register(self.lsock, selectors.EVENT_READ, data = None)
        while True:
            events = self.sel.select(timeout = None) #this blocks
            for key, mask in events:
                if key.data is None:
                    self.__accept_wrapper(key.fileobj)
                else:
                    self.__service_connection(key, mask)

   
    def listen_thread(self):
    # Starting the listen thread
        if not (self.t_listen.is_alive()):
            self.t_listen = threading.Thread(target = self.__listen)
            self.t_listen.start()
            print(str(self.t_listen.is_alive()))

    def __str__(self):
        return self.name
        

class Camera(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

class Frame(models.Model):
    name = models.CharField(max_length=30)
    content = bytes()

    def __str__(self):
        return self.name




