import boto3
import time


def detect_text_local_file(photo):

    client = boto3.client('rekognition')

    with open(photo, 'rb') as image:
        response = client.detect_text(Image={'Bytes': image.read()})

    with open(".\\results\\readme_aws.txt", "w", encoding='utf=8') as f:

        textDetections = response['TextDetections']
        print('Detected text\n----------')
        for text in textDetections:
            print(text['DetectedText'])
            print('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
            print('Id: {}'.format(text['Id']))
            if 'ParentId' in text:
                print('Parent Id: {}'.format(text['ParentId']))
            print('Type:' + text['Type'])
            print()

            if text["Type"] == "LINE":
                f.write(text["DetectedText"])
                f.write('\n')

    return len(textDetections)


def main():
    start_time = time.time()
    photo = 'images/whitespot.jpg'

    label_count = detect_text_local_file(photo)
    print("text detected: " + str(label_count))
    print("Elapsed time: {:.2f} seconds".format(time.time() - start_time))


if __name__ == "__main__":
    main()
