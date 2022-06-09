import Barcode
import Capture
import Dictionary

# Capture the image from the camera
Capture.capture()

# Scan the barcode from the saved image
Barcode.ScanBarcode()

# Calculate the price
price_before_tax = 0

# Check if the barcode is in the dictionary
if Barcode.item in Dictionary.Barcode_Dictionary.keys():
    price_before_tax += Dictionary.Barcode_Dictionary[Barcode.item][1]

# Calculate the price after tax
price_after_tax = 1.12 * price_before_tax

print(f"{'Name':<20} {'Price'}")
print(
    f"{Dictionary.Barcode_Dictionary[Barcode.item][0]:<20} {Dictionary.Barcode_Dictionary[Barcode.item][1]:.2f}"
)

print(f"{'Price before tax:':<20} {price_before_tax:.2f}")
print(f"{'Price after tax:':<20} {price_after_tax:.2f}")
