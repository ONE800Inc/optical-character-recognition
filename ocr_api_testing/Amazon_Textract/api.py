import boto3
import os
from os import path
import time

# Document

start_time = time.time()
current_dir = os.path.dirname(os.path.abspath(__file__))
image_file_name = "whitespot.jpg"
results_file_name = "results_awstextract.txt"
read_image_path = os.path.join(current_dir, "images", image_file_name)
result_path = os.path.join(current_dir, "results", results_file_name)

# Read document content
with open(read_image_path, 'rb') as document:
    imageBytes = bytearray(document.read())

# Amazon Textract client
textract = boto3.client('textract')

# Call Amazon Textract
response = textract.detect_document_text(Document={'Bytes': imageBytes})

# print(response)

with open(result_path, "w", encoding='utf=8') as f:

    # Print detected text
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            print('\033[94m' + item["Text"] + '\033[0m')
            f.write(item["Text"])
            f.write('\n')

print("Elapsed time: {:.2f} seconds".format(time.time() - start_time))
