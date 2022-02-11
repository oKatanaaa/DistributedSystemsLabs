## Description

This lab contains an example of sending an image using python sockets.
All the code is available in the `sockets.ipynb` notebook. For practice, another solution
with dockers is provided.

## Running docker solution

Ensure you have installed Docker and have it running. 
Do the following steps:
1. Run `build.bat` - it will create base docker image with all the necessary libraries set.
2. Go to `Server` folder and run `build.bat` - it will create image for the server.
3. Run `run.bat` - it launches the server's docker container.
4. Go to `Client` folder and run `build.bat` - it will create image for the client.
5. Run `run.bat` - it launches the client's docker container.

It is better to run everything from a terminal so that you can see all the messages.

The client container will send an image to the server container. The server container will
receive the image and print some info about information loss (which is not implemented at the moment).
