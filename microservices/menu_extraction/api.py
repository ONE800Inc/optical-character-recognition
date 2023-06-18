import argparse
import time
import os
import random

from google.cloud import vision

# Configure random number generator
random_number = random.randint(0, 100)

# Configure file paths
current_dir = os.path.dirname(os.path.abspath(__file__))
results_file_name = f"{random_number}results_google.txt"
result_path = os.path.join(current_dir, "results", results_file_name)

# Configure Google Cloud Vision API
def detect_text(path):
    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    print(texts[0].description)

    # Print each words and their bounding boxes
    # for i, text in enumerate(texts):
    #     print(f'\n"{text.description}"')
        
        # vertices = ([f'({vertex.x},{vertex.y})'
        #             for vertex in text.bounding_poly.vertices])

        # print('bounds: {}'.format(','.join(vertices)))

    # Write results to file
    # with open(result_path, "w", encoding='utf=8') as f:
    #     for s in range(1):
    #         f.write(texts[s].description)

    # Raise exception if error message
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

# Run the script
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("detect_file", help="The image for text detection.")
    parser.add_argument("-out_file", help="Optional output file", default=0)

    args = parser.parse_args()
    detect_text(args.detect_file)
