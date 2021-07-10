import os
import io
import socketserver
import socket
import selectors
import types
import threading
from threading import Condition


class camera():

    host = ''
    port = 65003
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sel = selectors.DefaultSelector()
    condition = Condition()
    buffer = io.BytesIO()
    frame = bytes()
    status = 'No Camera Connection'
    statusChange = Condition()
    frameInitialized = False
    t_listen = threading.Thread()
    cam_addr =''

    def __write(self, buf):
        
        if buf.startswith(b'\xff\xd8'):
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        
        return self.buffer.write(buf)
        
        # if self.frameInitialized == False:
        #     if buf.startswith(b'\xff\xd8'):
        #         self.buffer.truncate()
        #         self.buffer.seek(0)
        #         self.frameInitialized = True
        #         self.frame = self.buffer.getvalue()
        #         print(str(self.frameInitialized))
        #         return
        #     return

        # if (self.frameInitialized == True):
        #     if buf.startswith(b'\xff\xd8'):
        #         self.buffer.truncate()
        #         with self.condition:
        #             self.frame = self.buffer.getvalue()
        #             self.condition.notify_all()
        #           self.buffer.seek(0)
        #     return self.buffer.write(buf)
       #     

        

    def __accept_wrapper(self,sock):
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
                    self.__service_connection(
                        key, mask)

   
    def listen_thread(self):
    
        if not (self.t_listen.is_alive()):
            self.t_listen = threading.Thread(target = self.__listen)
            self.t_listen.start()
            print(str(self.t_listen.is_alive()))

        # t_listen = threading.Thread(target = self.__listen)
        # t_listen.start()
        




