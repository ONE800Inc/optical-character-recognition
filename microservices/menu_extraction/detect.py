import argparse
import time
import os
import random

from typing import MutableSequence
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
            width=5
        )
    return image

def get_document_bounds(image_file):
    """Returns document bounds given an image."""
    im = Image.open(image_file)
    w, h = im.size
    client = vision.ImageAnnotatorClient()

    bounds = []

    with open(image_file, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    objects = client.object_localization(image=image).localized_object_annotations

    for object_ in objects:
      indbounds = []
      for vertex in object_.bounding_poly.normalized_vertices:
        indbounds.append({'x': vertex.x * w,'y': vertex.y * h})

      bounds.append(indbounds)

    # The list `bounds` contains the coordinates of the bounding boxes.
    return bounds


def render_doc_text(filein, fileout):
    image = Image.open(filein)
    bounds = get_document_bounds(filein)
    # print(bounds)
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

def get_crop_hint(path: str) -> MutableSequence[vision.Vertex]:
    """Detect crop hints on a single image and return the first result.

    Args:
        path: path to the image file.

    Returns:
        The vertices for the bounding polygon.
    """
    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    crop_hints_params = vision.CropHintsParams(aspect_ratios=[1.77])
    image_context = vision.ImageContext(crop_hints_params=crop_hints_params)

    response = client.crop_hints(image=image, image_context=image_context)
    hints = response.crop_hints_annotation.crop_hints

    # Get bounds for the first crop hint using an aspect ratio of 1.77.
    vertices = hints[0].bounding_poly.vertices

    return vertices


def draw_hint(image_file: str) -> None:
    """Draw a border around the image using the hints in the vector list.

    Args:
        image_file: path to the image file.
    """
    vects = get_crop_hint(image_file)

    im = Image.open(image_file)
    draw = ImageDraw.Draw(im)
    draw.polygon(
        [
            vects[0].x,
            vects[0].y,
            vects[1].x,
            vects[1].y,
            vects[2].x,
            vects[2].y,
            vects[3].x,
            vects[3].y,
        ],
        None,
        "red",
        width=5
    )
    im.save("output-hint.jpg", "JPEG")
    print("Saved new image to output-hint.jpg")


def crop_to_hint(image_file: str) -> None:
    """Crop the image using the hints in the vector list.

    Args:
        image_file: path to the image file.
    """
    vects = get_crop_hint(image_file)

    im = Image.open(image_file)
    im2 = im.crop([vects[0].x, vects[0].y, vects[2].x - 1, vects[2].y - 1])
    im2.save("output-crop.jpg", "JPEG")
    print("Saved new image to output-crop.jpg")
    return im2
          
       
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("image_file", help="The image you'd like to crop.")
    parser.add_argument("mode", help='Set to "crop" or "draw".')

    args = parser.parse_args()
    
    if args.mode == "crop":
        crop_to_hint(args.image_file)
        localize_objects("output-crop.jpg")
        render_doc_text("output-crop.jpg", 0)
    elif args.mode == "draw":
        draw_hint(args.image_file)
    elif args.mode == "detect":
        localize_objects(args.image_file)
        render_doc_text(args.image_file, 0)
