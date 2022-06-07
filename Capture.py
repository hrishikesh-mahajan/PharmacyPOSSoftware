import cv2


def capture():

    cam_port = 0
    cam = cv2.VideoCapture(cam_port)

    # reading the input using the camera
    result, image = cam.read()

    # If image will detected without any error,
    # show result
    if result:

        # showing result, it take frame name and image
        # output
        cv2.imshow("Capture Barcode", image)

        # saving image in local storage
        cv2.imwrite("Input.png", image)

        # If keyboard interrupt occurs, destroy image
        # window
        cv2.waitKey(100)
        cv2.destroyWindow("Capture Barcode")

    # If captured image is corrupted, moving to else part
    else:
        print("No image detected. Please! try again")


# Driver Code
if __name__ == "__main__":
    capture()
