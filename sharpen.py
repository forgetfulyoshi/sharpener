"""
Author: Ben Anglin
Date: 10 April 2012
Course: CMSC 679 
"""
#! /usr/bin/python2

import argparse
import Image
import os

def quad_sharpen(image, window_x, window_y, threshold):
    """Sharpen based on a quadratic summation.

    Args:
        image : The input image. Type must be PIL.Image.
        window_x : The horizontal boundary over which to measure intensity.
        window_y : The vertical boundary over which to measure intensity.
        threshold : For every pixel in the produced image, if the original
            image's pixel intensity was above this value then it is set to 255 
            in the new image. If the original intensity was below this value, 
            then the new image's pixel is set to zero.

    Returns:
        A new image containing the sharpness mapping of the original. The type
        is also PIL.Image
    """
    rows = image.size[0]
    cols = image.size[1]
    current_image_access = image.load()
    new_image = Image.new(image.mode, image.size)
    new_image_access = new_image.load()

    for row in range(window_x + 2, rows - window_x):
        for col in range(window_y + 2, cols - window_y - 2):
            intensity = 0
            for u in range(0, window_x):
                for v in range (0, window_y):

                    step_1 = current_image_access[row + u, col + v]
                    step_2 = current_image_access[row + u - 2, col + v - 2]
                    intensity += pow(step_1 - step_2, 2)

            if intensity < threshold:
                new_image_access[row, col] = 0
            else:
                new_image_access[row, col] = 255

    return new_image


def abs_sharpen(image, window_x, window_y, threshold):
    """Sharpen based on an absolute value summation.

    Args:
        image : The input image. Type must be PIL.Image.
        window_x : The horizontal boundary over which to measure intensity.
        window_y : The vertical boundary over which to measure intensity.
        threshold : For every pixel in the produced image, if the original
            image's pixel intensity was above this value then it is set to 255 
            in the new image. If the original intensity was below this value, 
            then the new image's pixel is set to zero.

    Returns:
        A new image containing the sharpness mapping of the original. The type
        is also PIL.Image
    """
    rows = image.size[0]
    cols = image.size[1]
    current_image_access = image.load()
    new_image = Image.new(image.mode, image.size)
    new_image_access = new_image.load()

    for row in range(window_x, rows - window_x):
        for col in range(window_y, cols - window_y):
            intensity = 0
            for u in range(0, window_x):
                for v in range (0, window_y):

                    step_1 = current_image_access[row + u, col + v]
                    step_2= current_image_access[row + u - 1, col + v]
                    intensity += abs(step_1 - step_2)

            if intensity < threshold:
                new_image_access[row, col] = 0
            else:
                new_image_access[row, col] = 255

    return new_image


def sharpen(image_path, output_dir, window_x, window_y, threshold, style=''):
    """Generate an intensity image from a given image.
    
    Args:
        image_path : Path to original image file
        output_dir : Directory into which to place the intensity image.
        window_x : The horizontal boundary over which to measure intensity.
        window_y : The vertical boundary over which to measure intensity.
        threshold : For every pixel in the produced image, if the original
            image's pixel intensity was above this value then it is set to 255 
            in the new image. If the original intensity was below this value, 
            then the new image's pixel is set to zero.
        style : Method used to calculate intensity. Will default to quadratic.

    Yields:
        A new image in the specified directory. The image type will be the same
        as that of the input. The image name will be the same as the input with
        'intensity_' prepended.
    """
    if (image_path is None) or (output_dir is None):
        print "[-] Path to the image and the ouput directory must be supplied"
        return

    image_name = os.path.basename(image_path)
    image = Image.open(image_path)
    print "%s\n"\
          "[+] Format: %s\n"\
          "[+] Size: %s\n"\
          "[+] Mode: %s\n" % (image_name + '\n' + '=' * len(image_name), 
                              image.format, image.size, image.mode)

    if image.mode != 'L':
        image = image.convert('L')

    if style == 'abs':
        sharpened_image = abs_sharpen(image, window_x, window_y, threshold)
    else:
        sharpened_image = quad_sharpen(image, window_x, window_y, threshold)

    sharpened_image.save('intensity_' + image_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Sharpen an image")
    parser.add_argument('image', type=str, nargs=1, 
                        help="Path to the image file")

    parser.add_argument('-s', '--style', type=str, nargs=1, default=['quad'],
                        choices=['quad', 'abs'],
                        help="Method used for calculating intesity")

    parser.add_argument('-t', '--threshold', type=int, nargs=1, default=[10],
                        help="Intensity threshold [0,255]. Default is 10.")
    
    parser.add_argument('-x', type=int, nargs=1, default=[1],
                        help="Width of the sharpening window")
    
    parser.add_argument('-y', type=int, nargs=1, default=[1],
                        help="Hieght of the sharpening window")

    args = parser.parse_args()
    
    image_path = args.image.pop()
    abs_image_path = os.path.abspath(image_path) 
    
    style = args.style.pop()
    thresh = args.threshold.pop()
    x = args.x.pop()
    y = args.y.pop()

    sharpen(abs_image_path, os.getcwd(), x, y, thresh, style)
