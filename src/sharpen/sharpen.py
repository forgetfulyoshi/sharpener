#! /usr/bin/env python

from PIL import Image


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
                for v in range(0, window_y):
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
                for v in range(0, window_y):
                    step_1 = current_image_access[row + u, col + v]
                    step_2 = current_image_access[row + u - 1, col + v]
                    intensity += abs(step_1 - step_2)

            if intensity < threshold:
                new_image_access[row, col] = 0
            else:
                new_image_access[row, col] = 255

    return new_image


def sharpen(image, window_x, window_y, threshold, calc_style):
    """Generate an intensity image from a given image.
    
    Args:
        image (Image.Image): The original image, opened with Image.open()

        window_x (int): The horizontal boundary over which to measure intensity.

        window_y (int): The vertical boundary over which to measure intensity.

        threshold (int): For every pixel in the produced image, if the original
            image's pixel intensity was above this value then it is set to 255 
            in the new image. If the original intensity was below this value, 
            then the new image's pixel is set to zero.

        calc_style (str): Method used to calculate intensity. Either 'quad' or 'abs'.

    Returns:
        Image.Image: The sharpened image
    """

    print("[+] Format:", image.format)
    print("[+] Size:", image.size)
    print("[+] Mode:", image.mode)

    if image.mode != 'L':
        image = image.convert('L')

    if calc_style == 'abs':
        sharpened_image = abs_sharpen(image, window_x, window_y, threshold)
    elif calc_style == 'quad':
        sharpened_image = quad_sharpen(image, window_x, window_y, threshold)
    else:
        raise RuntimeError('Invalid intensity method: {}'.format(calc_style))

    return sharpened_image
