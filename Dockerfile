# Use the official AWS Lambda base image for Python 3.10
FROM public.ecr.aws/lambda/python:3.10

# Install necessary dependencies
RUN yum -y install git wget tar xz

# Download and install ffmpeg
RUN wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz \
    && tar xvf ffmpeg-release-amd64-static.tar.xz \
    && mv ffmpeg-*-amd64-static/ffmpeg /usr/bin/ffmpeg \
    && rm -Rf ffmpeg*

# Install required Python packages
RUN pip install --no-cache-dir setuptools-rust \
    && pip install --no-cache-dir git+https://github.com/openai/whisper.git

# Warm up the Whisper library
RUN whisper --model_dir /usr/local --model medium audio >> /dev/null 2>&1 || true

# Copy your app files
COPY app.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler
CMD [ "app.handler" ]
