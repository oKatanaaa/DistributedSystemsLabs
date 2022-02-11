FROM python:3
	RUN pip install opencv-python
	RUN apt-get update
	RUN apt-get install ffmpeg libsm6 libxext6  -y

	WORKDIR /usr/src/app
	COPY image_networker.py .

