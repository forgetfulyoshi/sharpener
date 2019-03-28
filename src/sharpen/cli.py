import click
from PIL import Image

from . import sharpen


# parser = argparse.ArgumentParser(description="Sharpen an image")
# parser.add_argument('image', type=str, nargs=1,
#                     help="Path to the image file")
#
# parser.add_argument('-s', '--style', type=str, nargs=1, default=['quad'],
#                     choices=['quad', 'abs'],
#                     help="Method used for calculating intesity")
#
# parser.add_argument('-t', '--threshold', type=int, nargs=1, default=[10],
#                     help="Intensity threshold [0,255]. Default is 10.")
#
# parser.add_argument('-x', type=int, nargs=1, default=[1],
#                     help="Width of the sharpening window")
#
# parser.add_argument('-y', type=int, nargs=1, default=[1],
#                     help="Hieght of the sharpening window")

@click.command()
@click.argument('infile', type=click.File('rb'))
@click.argument('outfile', type=click.File('wb'))
@click.option('--style', default='quad', help='Method used for intensity calculations')
@click.option('--threshold', type=int, default=10, help='Intensity threshold')
@click.option('-x', type=int, default=1, help='Width of the sharpening window')
@click.option('-y', type=int, default=1, help='Height of the sharpening window')
def sharpen_image(infile, outfile, style, threshold, x, y):
    image = Image.open(infile)
    result = sharpen.sharpen(image, x, y, threshold, style)
    result.save(outfile)


if __name__ == '__main__':
    sharpen_image()
