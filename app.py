import os
import shutil
import json
import urllib3
import urllib.parse
from urllib.parse import urlsplit
import whisper
import torch
import boto3
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


s3 = boto3.client("s3")


def handler(event, context):
    try:
        #print("Received event: " + json.dumps(event, indent=2))
        
        # Configuring a variable needed by Huggingface
        #os.environ["TRANSFORMERS_CACHE"] = "/tmp/data"
        #model = whisper.load_model("base")
        #logger.info("Model is up")
        
        s3_url = "s3://matchmaking-automation-experiment/VolkswagenGTIReview.mp4"
        
        # Use urlsplit to break down the URL into components
        url_components = urlsplit(s3_url)

        # Extract bucket and key from the components
        bucket = url_components.netloc
        key = url_components.path.lstrip('/')
        
        logger.info(f"Bucket: {bucket}, key: {key}")

        # Define the new folder /tmp/data
        os.makedirs("/tmp/data", exist_ok=True)

        audio_file = '/tmp/data/{}'.format(key)
        logging.info(f"Audio file: {audio_file}")
        
        os.chdir('/tmp/data')
        
        # Downloading file to transcribe
        s3.download_file(bucket, key, audio_file)
        
        # Configuring a variable needed by Huggingface
        os.environ["TRANSFORMERS_CACHE"] = "/tmp/data"

        model = whisper.load_model("base", download_root="/tmp/data")
        logger.info("Model is up")
        result = model.transcribe(audio_file, fp16=False)
        
        logger.info(result)
        
        return {
            "statusCode": 200,
            "body": json.dumps(result["text"])
        }
    except TabError as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps("Error processing the file")
        }