import argparse
import time


def detect_text(path):
    from google.cloud import vision
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

    with open(".\\results\\readme_goog.txt", "w", encoding='utf=8') as f:
        for s in range(1):
            f.write(texts[s].description)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


def run_local(args):
    if args.command == 'text':
        start_time = time.time()
        detect_text(args.path)
        print("Elapsed time: {} seconds".format(time.time() - start_time))

    # add more commands


start_time = time.time()
detect_text("./images/whitespot.jpg")
print("Elapsed time: {} seconds".format(time.time() - start_time))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command')

    detect_text_parser = subparsers.add_parser(
        'text', help=detect_text.__doc__)
    detect_text_parser.add_argument('path')

    args = parser.parse_args()

    run_local(args)
