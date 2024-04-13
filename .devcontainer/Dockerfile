# set base image (host OS)
FROM python:3.12

# set the working directory in the container
WORKDIR /workspaces/plat-analysis

RUN apt update
RUN apt install -y tesseract-ocr libtesseract-dev libpoppler-cpp-dev poppler-utils ffmpeg libsm6 libxext6
RUN make build