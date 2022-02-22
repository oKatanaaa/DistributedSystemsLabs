import socket
import cv2
import numpy as np
from random import random

from image_networker import ImageNetworker, HOST

NOISE_HOST = 'lab1_noise_server'
CLEAN_HOST = 'lab1_server'

class NoiseServer(ImageNetworker):
    def __init__(self, fake_server_port, real_server_port, block_size=1024):
        super().__init__(block_size, 'NoiseServer')
        # Receives image from the client
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv_socket.bind((NOISE_HOST, fake_server_port))
        self.recv_socket.listen()
        self.fake_server_port = fake_server_port
        
        # Sends image to the server
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.real_server_port = real_server_port
        
    def run(self):
        with self.recv_socket as s:
            self.log(f'Accepting {self.fake_server_port}')
            conn, addr = s.accept()
            self.log('Connected. Receiving image.')
            image = self.recv_image(conn)
        
        noise_image = self.add_noise(image)
        with self.send_socket as s:
            s.connect((CLEAN_HOST, self.real_server_port))
            self.send_image(image, s)
            self.send_image(noise_image, s)
        
    def add_noise(self, im):
        im = im.copy()
        h, w, _ = im.shape
        for y in range(h):
            for x in range(w):
                if random() > 0.9:
                    im[y, x] = int(random() > 0.5) * 255
        return im

if __name__ == '__main__':
    server = NoiseServer(
        fake_server_port=65000,
        real_server_port=65001,
    )
    server.start()

