import cv2
from pyzbar.pyzbar import decode

image_path = "Product.png"


def barcode_reader(image):
    img = cv2.imread(str(image))
    detected_barcodes = decode(img)
    if not detected_barcodes:
        return 0
    else:
        for barcode in detected_barcodes:
            if barcode.data != "":
                return int(barcode.data)


def capture():
    # 0 for native, 1 for DroidCam
    cam_port = 0
    cam = cv2.VideoCapture(cam_port, cv2.CAP_DSHOW)
    while True:
        result, captured_image = cam.read()
        cv2.imwrite(image_path, captured_image)
        cv2.imshow("Capture Barcode", captured_image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        item = barcode_reader(image_path)
        if item:
            break
    cam.release()
    cv2.destroyAllWindows()
    return item


if __name__ == "__main__":
    capture()
