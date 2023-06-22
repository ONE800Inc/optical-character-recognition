import cv2


try:
    import azure.ai.vision as visionsdk
except ImportError:
    print("""
    Importing Azure AI Vision SDK for Python failed.
    Refer to README.md in this directory for installation instructions.
    """)
    import sys
    sys.exit(1)

"""
This sample does analysis on an image file using all visual features
and a synchronous (blocking) call. It prints the results to the console,
including the detailed results.
"""


def image_analysis_sample_analyze(img_name):
    """
    Analyze image from file, all features, synchronous (blocking)
    """

    service_options = visionsdk.VisionServiceOptions(
        key="aed617482e9a40b08651ad8ed0c084c7", endpoint="https://one800ocr.cognitiveservices.azure.com/")

    # Specify the image file on disk to analyze. sample1jpg is a good example to show most features
    vision_source = visionsdk.VisionSource(filename=img_name)

    # Or, instead of the above, specify a publicly accessible image URL to analyze. For example:
    # image_url = "https://learn.microsoft.com/azure/cognitive-services/computer-vision/images/windows-kitchen.jpg"
    # vision_source = visionsdk.VisionSource(url=image_url)

    # Set the language and one or more visual features as analysis options
    analysis_options = visionsdk.ImageAnalysisOptions()

    # Mandatory. You must set one or more features to analyze. Here we use the full set of features.
    # Note that "CAPTION" and "DENSE_CAPTIONS" are only supported in Azure GPU regions (East US, France Central,
    # Korea Central, North Europe, Southeast Asia, West Europe, West US). Remove "CAPTION" and "DENSE_CAPTIONS"
    # from the list below if your Computer Vision key is not from one of those regions.
    analysis_options.features = (
        visionsdk.ImageAnalysisFeature.CROP_SUGGESTIONS |
        visionsdk.ImageAnalysisFeature.CAPTION |
        visionsdk.ImageAnalysisFeature.DENSE_CAPTIONS |
        visionsdk.ImageAnalysisFeature.OBJECTS |
        visionsdk.ImageAnalysisFeature.PEOPLE |
        visionsdk.ImageAnalysisFeature.TEXT |
        visionsdk.ImageAnalysisFeature.TAGS
    )

    # Optional, and only relevant when you select ImageAnalysisFeature.CROP_SUGGESTIONS.
    # Define one or more aspect ratios for the desired cropping. Each aspect ratio needs
    # to be in the range [0.75, 1.8]. If you do not set this, the service will return one
    # crop suggestion with the aspect ratio it sees fit.
    analysis_options.cropping_aspect_ratios = [1.0]

    # Optional. Default is "en" for English. See https://aka.ms/cv-languages for a list of supported
    # language codes and which visual features are supported for each language.
    analysis_options.language = "en"

    # Optional. Default is "latest".
    analysis_options.model_version = "latest"

    # Optional, and only relevant when you select ImageAnalysisFeature.CAPTION.
    # Set this to "true" to get a gender neutral caption (the default is "false").
    analysis_options.gender_neutral_caption = True

    # Create the image analyzer object
    image_analyzer = visionsdk.ImageAnalyzer(
        service_options, vision_source, analysis_options)

    # Do image analysis for the specified visual features
    print()
    print(" Please wait for image analysis results...")
    print()

    # This call creates the network connection and blocks until Image Analysis results
    # return (or an error occurred). Note that there is also an asynchronous (non-blocking)
    # version of this method: image_analyzer.analyze_async().
    result = image_analyzer.analyze()

    # Checks result.
    if result.reason == visionsdk.ImageAnalysisResultReason.ANALYZED:

        print(" Image height: {}".format(result.image_height))
        print(" Image width: {}".format(result.image_width))
        print(" Model version: {}".format(result.model_version))

        if result.caption is not None:
            print(" Caption:")
            print("   '{}', Confidence {:.4f}".format(
                result.caption.content, result.caption.confidence))

        if result.dense_captions is not None:
            print(" Dense Captions:")
            for caption in result.dense_captions:
                print("   '{}', {}, Confidence: {:.4f}".format(
                    caption.content, caption.bounding_box, caption.confidence))

        if result.objects is not None:
            print(" Objects:")
            for object in result.objects:
                print("   '{}', {}, Confidence: {:.4f}".format(
                    object.name, object.bounding_box, object.confidence))

        if result.tags is not None:
            print(" Tags:")
            for tag in result.tags:
                print("   '{}', Confidence {:.4f}".format(
                    tag.name, tag.confidence))

        if result.people is not None:
            print(" People:")
            for person in result.people:
                print("   {}, Confidence {:.4f}".format(
                    person.bounding_box, person.confidence))

        if result.crop_suggestions is not None:
            print(" Crop Suggestions:")
            for crop_suggestion in result.crop_suggestions:
                print("   Aspect ratio {}: Crop suggestion {}"
                      .format(crop_suggestion.aspect_ratio, crop_suggestion.bounding_box))

        if result.text is not None:
            print(" Text:")
            for line in result.text.lines:
                points_string = "{" + ", ".join([str(int(point))
                                                for point in line.bounding_polygon]) + "}"
                print("   Line: '{}', Bounding polygon {}".format(
                    line.content, points_string))
                for word in line.words:
                    points_string = "{" + ", ".join([str(int(point))
                                                    for point in word.bounding_polygon]) + "}"
                    print("     Word: '{}', Bounding polygon {}, Confidence {:.4f}"
                          .format(word.content, points_string, word.confidence))

        result_details = visionsdk.ImageAnalysisResultDetails.from_result(
            result)
        print(" Result details:")
        print("   Image ID: {}".format(result_details.image_id))
        print("   Result ID: {}".format(result_details.result_id))
        print("   Connection URL: {}".format(result_details.connection_url))
        print("   JSON result: {}".format(result_details.json_result))

        x = crop_suggestion.bounding_box.x
        y = crop_suggestion.bounding_box.y
        x2 = crop_suggestion.bounding_box.h
        y2 = crop_suggestion.bounding_box.w

        img = cv2.imread(img_name)

        # make the window resizable
        cv2.namedWindow(img_name, cv2.WINDOW_NORMAL)

        cv2.rectangle(img, (x, y), (x2, y2), (0, 255, 0), 7)

        cv2.imwrite(img_name, img)
        cv2.imshow(img_name, img)
        k = cv2.waitKey(0)
        if k == 27:         # wait for ESC key to exit
            cv2.destroyAllWindows()

    else:

        error_details = visionsdk.ImageAnalysisErrorDetails.from_result(result)
        print(" Analysis failed.")
        print("   Error reason: {}".format(error_details.reason))
        print("   Error code: {}".format(error_details.error_code))
        print("   Error message: {}".format(error_details.message))
        print(" Did you set the computer vision endpoint and key?")


image_analysis_sample_analyze(img_name='newyork.jpg')
