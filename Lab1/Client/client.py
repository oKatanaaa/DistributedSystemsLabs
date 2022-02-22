import socket
import cv2

from image_networker import ImageNetworker, HOST

HOST = 'lab1_noise_server'

class Client(ImageNetworker):
    def __init__(self, server_port, image, block_size=1024):
        super().__init__(block_size, 'Client')
        self.port = server_port
        self.image = image
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def run(self):
        with self.socket as s:
            self.log(f'Connecting to server with port {self.port}')
            s.connect((HOST, self.port))
            self.log('Connected. Sending image.')
            self.send_image(self.image, self.socket)


if __name__ == '__main__':
    im = cv2.imread('img.jpg')
    client = Client(server_port=65000, image=im)
    client.start()
