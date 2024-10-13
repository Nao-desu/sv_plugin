# This file is used to convert jpg to png.
from os import path
from PIL import Image
import os
import rich
import rich.progress


PATH = path.dirname(__file__)

def convert_png_to_jpg(png_path):
    IMG = Image.open(png_path)
    jpg_path = png_path.replace('.png', '.jpg')
    IMG.convert('RGB').save(jpg_path,"JPEG")
    os.remove(png_path)
    
#文件夹
folder = ["C","E","full"]

def main():
    all_png = []
    for i in folder:
        f_path = path.join(PATH, 'img' ,i)
        for file in os.listdir(f_path):
            if file.endswith('.png'):
                all_png.append(path.join(f_path, file))
    #构建进度条
    with rich.progress.Progress() as progress:
        task = progress.add_task("Converting PNG to JPG", total=len(all_png))
        for png in all_png:
            progress.update(task, advance=1)
            convert_png_to_jpg(png)
            
if __name__ == '__main__':
    main()