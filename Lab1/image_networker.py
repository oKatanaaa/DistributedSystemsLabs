import socket
from multiprocessing.dummy import Process
import time
import cv2
import numpy as np

HOST = ''

class ImageNetworker(Process):
    """
    Contains utilities for sending/receiving images using sockets.
    """
    def __init__(self, block_size=1024, name='networker'):
        super().__init__()
        self.block_size = block_size
        self.name = name
    
    def log(self, *args):
        print(f'{self.name} /', *args)
        
    # --- SENDING
    def send_image(self, image, socket):
        n_bytes = self.send_image_meta(image, socket)
        n_iters = n_bytes // self.block_size
        n_remains = n_bytes - n_iters * self.block_size
        im_bytes = image.tobytes()
        for i in range(n_iters):
            block = im_bytes[self.block_size * i: (i+1) * self.block_size]
            assert socket.sendall(block) is None, f'Could not send image byte block i={i}'
        
        if n_remains > 0:
            block = im_bytes[-n_remains:]
            assert socket.sendall(block) is None, f'Could not send remaining byte block'
        
        self.log('Image is sent.')
        
    def send_image_meta(self, image, socket):
        h, w, _ = image.shape
        n_bytes = h * w * 3  # 3 channels
        bytes_array = image.tobytes()
        
        # --- Send image meta info
        # 1. N_Bytes
        assert self.send_int(n_bytes, socket) is None, 'Could not send n_bytes'
        # 2. height
        assert self.send_int(h, socket) is None, 'Could not send height'
        # 3. width
        assert self.send_int(w, socket) is None, 'Could not send width'
        return n_bytes
    
    def send_int(self, number, socket):
        _bytes = number.to_bytes(length=4, byteorder='big')
        return socket.sendall(_bytes)
    
    # --- RECEIVING
    
    def recv_image(self, conn):
        n_bytes, h, w = self.recv_image_meta(conn)
        n_iters = n_bytes // self.block_size
        n_remains = n_bytes - n_iters * self.block_size
        im_bytes = []
        n_received = 0
        while True:
            block = conn.recv(self.block_size)
            im_bytes.append(block)
            n_received += len(block)
            
            if n_received == n_bytes:
                break
  
        im_bytes = b''.join(im_bytes)
        image = np.frombuffer(im_bytes, dtype='uint8')
        image = image.reshape(h, w, 3)
        #self.assert_success()
        print(f'Received image with size={h, w}.')
        return image
            
    def recv_image_meta(self, conn):
        # --- Recv image meta info
        # 1. N_Bytes
        n_bytes = self.recv_int(conn)
        # 2. height
        h = self.recv_int(conn)
        # 3. width
        w = self.recv_int(conn)
        return n_bytes, h, w
    
    def recv_int(self, conn):
        _bytes = conn.recv(4)
        return int.from_bytes(_bytes, byteorder='big')
