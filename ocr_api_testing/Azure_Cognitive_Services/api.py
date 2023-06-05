# <snippet_imports_and_vars>
# <snippet_imports>
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
# </snippet_imports>

'''
Authenticate
Authenticates your credentials and creates a client.
'''
# <snippet_vars>
subscription_key = "aed617482e9a40b08651ad8ed0c084c7"
endpoint = "https://one800ocr.cognitiveservices.azure.com/"
# </snippet_vars>
# </snippet_imports_and_vars>

# <snippet_client>
computervision_client = ComputerVisionClient(
    endpoint, CognitiveServicesCredentials(subscription_key))
# </snippet_client>
'''
END - Authenticate
'''

# <snippet_read_call>
'''
OCR: Read File using the Read API, extract text - remote
This example will extract text in an image, then print results, line by line.
This API call can also extract handwriting style text (not shown).
'''
# print("===== Read File - remote =====")
# # Get an image with text
# read_image_url = "https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/master/articles/cognitive-services/Computer-vision/Images/readsample.jpg"

# # Call API with URL and raw response (allows you to get the operation location)
# read_response = computervision_client.read(read_image_url,  raw=True)
# # </snippet_read_call>

# # <snippet_read_response>
# # Get the operation location (URL with an ID at the end) from the response
# read_operation_location = read_response.headers["Operation-Location"]
# # Grab the ID from the URL
# operation_id = read_operation_location.split("/")[-1]

# # Call the "GET" API and wait for it to retrieve the results
# while True:
#     read_result = computervision_client.get_read_result(operation_id)
#     if read_result.status not in ['notStarted', 'running']:
#         break
#     time.sleep(1)

# # Print the detected text, line by line
# if read_result.status == OperationStatusCodes.succeeded:
#     for text_result in read_result.analyze_result.read_results:
#         for line in text_result.lines:
#             print(line.text)
#             print(line.bounding_box)
# print()
# </snippet_read_response>
'''
END - Read File - remote
'''

'''
OCR: Read File using the Read API, extract text - local
This example extracts text from a local image, then prints results.
This API call can also recognize remote image text (shown in next example, Read File - remote).
'''
print("===== Read File - local =====")
# start timer
start_time = time.time()
# Get image path
current_dir = os.path.dirname(os.path.abspath(__file__))

image_file_name = "french2.jpg"
results_file_name = "results_azure.txt"

read_image_path = os.path.join(current_dir, "images", image_file_name)
result_path = os.path.join(current_dir, "results", results_file_name)
# Open the image
read_image = open(read_image_path, "rb")

# Call API with image and raw response (allows you to get the operation location)
read_response = computervision_client.read_in_stream(read_image, raw=True)
# Get the operation location (URL with ID as last appendage)
read_operation_location = read_response.headers["Operation-Location"]
# Take the ID off and use to get results
operation_id = read_operation_location.split("/")[-1]

# Call the "GET" API and wait for the retrieval of the results
while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status.lower() not in ['notstarted', 'running']:
        break
    print('Waiting for result...')
    time.sleep(1)

with open(result_path, "w", encoding='utf=8') as f:

    # Print results, line by line
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                print(line.text)
                f.write(line.text)
                f.write("\n")

print()
# print the elapsed time
print("Elapsed time: {:.2f} seconds".format(time.time() - start_time))
'''
END - Read File - local
'''
