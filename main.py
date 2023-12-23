from PIL import Image
from argparse import ArgumentParser
from sys import argv
from os import path, listdir
from pillow_heif import register_heif_opener

COMPILE_COMMAND = 'pyinstaller --onefile --name "imageconvert" .\main.py'

argument_parser = ArgumentParser(prog='HEIC to JPEG converter', description='Converts HEIC pictures to PNG')
argument_parser.add_argument('filename') 
argument_parser.add_argument('-f', '--filepaths', help='The images that you need converted', nargs='*', required=True)
argument_parser.add_argument('-e', '--extension', help='The file extension that you want as a result', choices=['.heic', '.jpeg', '.png'], required=True)
argument_parser.add_argument('-t', '--to', help='The folder that you want your converted images to go in', default='', required=False)

register_heif_opener()

def convert_to_png(filepath: str):
    if path.isdir(filepath):
        for i in listdir(filepath):
            convert_to_png(filepath + '/' + i)
        return

    png_filename, _ = path.splitext(path.split(filepath)[1])
    png_filename += '.png'

    try:
        image = Image.open(filepath)
    except FileNotFoundError:
        print(f'File {filepath} not found. Passing to next file')
        return

    print(f'Converting {filepath} to png...')

    if path.exists(png_filename):
        print(f'File {png_filename} already exists. Passing to next file')
        return
    
    image.save(args.to + png_filename)

def convert_to_jpeg(filepath: str):
    if path.isdir(filepath):
        for i in listdir(filepath):
            convert_to_jpeg(filepath + '/' + i)
        return

    jpeg_filename, _ = path.splitext(path.split(filepath)[1])
    jpeg_filename  += '.jpeg'

    try:
        image = Image.open(filepath)
    except FileNotFoundError:
        print(f'File {filepath} not found. Passing to next file')
        return

    print(f'Converting {filepath} to jpeg...')

    if path.exists(jpeg_filename):
        print(f'File {jpeg_filename} already exists. Passing to next file')
        return

    jpg_im = image.convert('RGB')
    jpg_im.save(args.to + jpeg_filename)

def convert_to_heic(filepath: str):
    if path.isdir(filepath):
        for i in listdir(filepath):
            convert_to_heic(filepath + '/' + i)
        return

    heic_filename, _ = path.splitext(path.split(filepath)[1])
    heic_filename += '.HEIC'

    try:
        image = Image.open(filepath)
    except FileNotFoundError:
        print(f'File {filepath} not found. Passing to next file')
        return

    print(f'Converting {filepath} to heic...')

    if path.exists(heic_filename):
        print(f'File {heic_filename} already exists. Passing to next file')
        return

    image.save(args.to + heic_filename)

if __name__ == '__main__':
    args = argument_parser.parse_args(argv)
    filepaths: list[str] = args.filepaths
    extension = args.extension

    if args.to != '' and not path.exists(args.to):
        raise RuntimeError(f'Cannot find folder {args.to}')

    if extension == '.png':
        for i in filepaths:
            convert_to_png(i)
    elif extension == '.jpeg':
        for i in filepaths:
            convert_to_jpeg(i)
    elif extension == '.heic':
        for i in filepaths:
            convert_to_heic(i)
