
import os
from PIL import Image

from ValidImageFormats import valid_formats
from AsciiBrightnessScale import ascii_brightness_scale

def get_brightness_values(image_data):
    """
    Takes a list of tuples, each tuple containing RGB values,
     and returns a list with the brightness value of every tuplet.  
    """
    pixels_brightness_value = []

    for pixel in image_data:
        r = pixel[0]
        g = pixel[1]
        b = pixel[2]
        # Formula to get the general brightness value
        brightness = 0.33*r + 0.5*g + 0.16*b
        brightness = int(round(brightness, 0))
        pixels_brightness_value.append(brightness)
    
    return pixels_brightness_value


def print_ascii_image(
        brightness_values,
        image_width,
        brightness_scale):
    """
    Takes the list created with get_brightness_values(), the width of the
    image (int) and the brightness scale (string) selected by the user to
     print the ASCII reproduction of the original image on console.
    """
    for index, pixel_value in enumerate(brightness_values):
        if index % image_width == 0 and index != 0:
            print("")
        
        if pixel_value == 0:
            pixel_range = pixel_value
        else:
            pixel_range = int(pixel_value / (255 / len(brightness_scale)))

        print(brightness_scale[pixel_range], end=" ")


def main():
    # Image path 
    image = input("Image path: ")
    if not os.path.isfile(image):
        raise FileNotFoundError("The file path does not exist.")

    file_extension = os.path.splitext(image)[1]
    if file_extension not in valid_formats:
        raise IOError("The file is not a supported image file format.For supported formats check the file 'ValidImageFormats'.")

    # Get how many ASCII characters can the image representation use
    bright_key = input("Select the amount of usable ascii symbols in the image, the brightness scale (1 - 25): ")

    if bright_key not in ascii_brightness_scale:
        raise IOError("The value for the brightness scale must be between 1 and 25 inclusive.")

    brightness_scale = ascii_brightness_scale[bright_key]

    # Load image
    with Image.open(image).convert('RGB') as im:
        print(f"Actual image size (w, h) is {im.size[0]}x{im.size[1]}.")
        
        # Resize image if requested
        do_resize = input("Resize image? (Y/n): ").upper()
        if do_resize == "Y":
            image_width = int(input("New width: "))
            image_height = int(input("New height: "))
            im = im.resize((image_width, image_height))

        # Get image data
        image_data = list(im.getdata())
        image_width = im.size[0]
        image_height = im.size[1]

        # Iterate through all the pixel and store its brightness value on a list
        pixels_brightness_value = get_brightness_values(image_data)
        
        # Clear console screen for a clean image
        os.system('cls')

        # Print the ASCII image
        print_ascii_image(pixels_brightness_value, image_width, brightness_scale)

    input("")

if __name__ == "__main__":
    main()