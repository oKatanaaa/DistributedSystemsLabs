## Description

This lab contains an example of sending an image using python sockets.
All the code is available in the `sockets.ipynb` notebook. For practice, another solution
with dockers is provided.

## Running docker solution

Ensure you have installed Docker and have it running. 
Do the following steps:
1. Run `build.bat` - it will create base docker image with all the necessary libraries set.
2. Go to `Server` folder and run `build.bat` and `run.bat` - it will create image for the server and launch the
corresponding docker container.
3. Go to `NoiseServer` folder and run `build.bat` and `run.bat` (same as Server).
4. Go to `Client` folder and run `build.bat` and `run.bat` (same as Server).

It is better to run everything from a terminal so that you can see all the messages.

Messaging between containers is as follows:
Client -> NoiseServer -> Server.
1. Client connects to socket on port 65000 and sends an image.
2. NoiseServer listens on port 65000, receives image and adds noise.
3. NoiseServer connects to socket on port 65001 and sends both original image and the corrupted one.
4. Server listens on port 65001, receives both images and performs restoration of the corrupted one.
It also prints some info regarding the restoration quality.

