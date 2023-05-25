import argparse
import time
import os
import random

from enum import Enum
from google.cloud import vision
from PIL import Image, ImageDraw

random_number = random.randint(0, 100)
current_dir = os.path.dirname(os.path.abspath(__file__))

# image_file_name = "menu2.jpg"
results_file_name = f"{random_number}results_google.txt"

# read_image_path = os.path.join(current_dir, "images", image_file_name)
result_path = os.path.join(current_dir, "results", results_file_name)


def detect_text(path):
    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print(f'\n"{text.description}"')

        vertices = ([f'({vertex.x},{vertex.y})'
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    with open(result_path, "w", encoding='utf=8') as f:
        for s in range(1):
            f.write(texts[s].description)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5


def draw_boxes(image, bounds, color):
    """Draw a border around the image using the hints in the vector list."""
    draw = ImageDraw.Draw(image)

    for bound in bounds:
        draw.polygon(
            [
                bound.vertices[0].x,
                bound.vertices[0].y,
                bound.vertices[1].x,
                bound.vertices[1].y,
                bound.vertices[2].x,
                bound.vertices[2].y,
                bound.vertices[3].x,
                bound.vertices[3].y,
            ],
            None,
            color,
        )
    return image


def get_document_bounds(image_file, feature):
    """Returns document bounds given an image."""
    client = vision.ImageAnnotatorClient()

    bounds = []

    with open(image_file, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    # Collect specified feature bounds by enumerating all document features
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if feature == FeatureType.SYMBOL:
                            bounds.append(symbol.bounding_box)

                    if feature == FeatureType.WORD:
                        bounds.append(word.bounding_box)

                if feature == FeatureType.PARA:
                    bounds.append(paragraph.bounding_box)

            if feature == FeatureType.BLOCK:
                bounds.append(block.bounding_box)

    # The list `bounds` contains the coordinates of the bounding boxes.
    return bounds


def render_doc_text(filein, fileout):
    image = Image.open(filein)
    bounds = get_document_bounds(filein, FeatureType.BLOCK)
    draw_boxes(image, bounds, "blue")
    bounds = get_document_bounds(filein, FeatureType.PARA)
    draw_boxes(image, bounds, "red")
    bounds = get_document_bounds(filein, FeatureType.WORD)
    draw_boxes(image, bounds, "yellow")

    # save image to a new file
    if fileout != 0:
        image.save(fileout)
    else:
        image.save(f"results/{random_number}output.jpg")
        image.show()

# start_time = time.time()
# detect_text(read_image_path)
# print("Elapsed time: {} seconds".format(time.time() - start_time))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("detect_file", help="The image for text detection.")
    parser.add_argument("-out_file", help="Optional output file", default=0)

    args = parser.parse_args()
    render_doc_text(args.detect_file, args.out_file)
    detect_text(args.detect_file)
