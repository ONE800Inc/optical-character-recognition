import boto3
import os
from os import path
import time

# Document

start_time = time.time()
file_dir = os.path.dirname(os.path.realpath('__file__'))
documentName = os.path.join(file_dir, ".\images\whitespot.jpg")

# Read document content
with open(documentName, 'rb') as document:
    imageBytes = bytearray(document.read())

# Amazon Textract client
textract = boto3.client('textract')

# Call Amazon Textract
response = textract.detect_document_text(Document={'Bytes': imageBytes})

# print(response)

with open(".\\results\\readme_aws.txt", "w", encoding='utf=8') as f:

    # Print detected text
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            print('\033[94m' + item["Text"] + '\033[0m')
            f.write(item["Text"])
            f.write('\n')

print("Elapsed time: {:.2f} seconds".format(time.time() - start_time))
