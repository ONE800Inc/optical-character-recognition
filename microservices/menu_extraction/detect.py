import argparse
import time
import os
import random

from enum import Enum
from google.cloud import vision
from PIL import Image, ImageDraw

# Configure random number generator
random_number = random.randint(0, 100)

# Configure file paths
current_dir = os.path.dirname(os.path.abspath(__file__))
results_file_name = f"{random_number}results_google.txt"
result_path = os.path.join(current_dir, "results", results_file_name)

def draw_boxes(image, bounds, color):
    """Draw a border around the image using the hints in the vector list."""
    draw = ImageDraw.Draw(image)

    for bound in bounds:
        draw.polygon(
            [
                bound[0]['x'],
                bound[0]['y'],
                bound[1]['x'],
                bound[1]['y'],
                bound[2]['x'],
                bound[2]['y'],
                bound[3]['x'],
                bound[3]['y'],
            ],
            None,
            color,
        )
    return image

def get_document_bounds(image_file):
    """Returns document bounds given an image."""
    client = vision.ImageAnnotatorClient()

    bounds = []

    with open(image_file, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    objects = client.object_localization(image=image).localized_object_annotations

    for object_ in objects:
      indbounds = []
      for vertex in object_.bounding_poly.normalized_vertices:
        indbounds.append({'x': vertex.x * 600,'y': vertex.y * 800})

      bounds.append(indbounds)

    # The list `bounds` contains the coordinates of the bounding boxes.
    return bounds


def render_doc_text(filein, fileout):
    image = Image.open(filein)
    bounds = get_document_bounds(filein)
    print(bounds)
    draw_boxes(image, bounds, "red")

    # save image to a new file
    if fileout != 0:
        image.save(fileout)
    else:
        image.save(f"results/{random_number}output.jpg")
        image.show()

def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(image=image).localized_object_annotations

    print(f"Number of objects found: {len(objects)}")
    for object_ in objects:
        print(f"\n{object_.name} (confidence: {object_.score})")
        print("Normalized bounding polygon vertices: ")
        for vertex in object_.bounding_poly.normalized_vertices:
            print(f" - ({vertex.x}, {vertex.y})")
          
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("detect_file", help="The image for text detection.")
    parser.add_argument("-out_file", help="Optional output file", default=0)

    args = parser.parse_args()
    localize_objects(args.detect_file)
    render_doc_text(args.detect_file, args.out_file)
    
    
