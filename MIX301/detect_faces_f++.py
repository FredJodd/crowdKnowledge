import cv2
import argparse
import requests
import util
import simplejson


def draw_face_rects(image, api_key, api_secret):
    # Connect to F++-api and provide key, secret and image file
    fpp_detect_url = "https://api-us.faceplusplus.com/facepp/v3/detect?api_key={k}&api_secret={s}"
    r = requests.post(fpp_detect_url.format(k=api_key, s=api_secret), files={"image_file": open(image_path, "rb")})

    # Load the result into a JSON-dictionary
    json = simplejson.loads(r.text)

    # If the JSON only has one key then it failed
    if len(json) is 1:
        # Print error message and quit
        print("Error: " + json["error_message"])
        exit(1)

    for face in json["faces"]:
        image = util.draw_rect_copy(image, face["face_rectangle"])

    return image


if __name__ == "__main__":
    # Define input arguments for the script
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image_path", type=str, help="Path to image file")
    parser.add_argument("-k", "--api_key", type=str, help="API key for F++")
    parser.add_argument("-s", "--api_secret", type=str, help="API secret F++")

    # Parse the arguments
    args = parser.parse_args()
    image_path = args.image_path
    fpp_key = args.api_key
    fpp_secret = args.api_secret

    # Validate the input arguments and quit if invalid
    util.quit_if_file_arg_is_invalid(image_path, "Must provide a valid image file")

    # Load image
    input_image = cv2.imread(image_path)

    util.show_image("Detect faces: Face++", draw_face_rects(input_image, fpp_key, fpp_secret))
