import os
from PIL import Image
import numpy as np

"""
This is a basic python script that generates a dataset to test a segmentation model
It takes a folder of transparent pngs as input and generates a mask image and a noise background image.

I used this to test my network visualisation script quickly NOT architecture performance.
The noise background image provides more challenge than a plain background so resultant kernels are interesting (edge detection not just plain).
"""

# Seed data should be in a nested folder labelled Transparent
# I used pokemon sprite pngs I ripped from the internet
working = 'Datasets\Pokemon'

def main(working):
    # Folder vars
    dir_transparent = f'{working}\\Transparent'
    dir_mask = f'{working}\\Mask'
    dir_noise = f'{working}\\Noise'

    # Check dataset files exist.
    if not os.path.exists(working):
        raise Exception(f'Cannot find working directory at {working}')
    if not os.path.exists(working+'\Transparent'):
        raise Exception(f'Cannot find folder named "Transparent" in {working}')

    # Create new folders
    # Not allowing old folders as this can mess up the dataloader if there are mismatched files etc.
    try:
        os.makedirs(dir_mask)
    except FileExistsError:
        raise FileExistsError(f"Warning: Mask directory in {working} already exists")
    try:
        os.makedirs(dir_noise)
    except FileExistsError:
        raise FileExistsError(f"Warning: Noise directory in {working} already exists")


    for file in os.listdir(dir_transparent):
        print(f"Working on file {file}")
        img = Image.open(f'{dir_transparent}\\{file}')
        # Ensure RGBA and resize images
        x_size = y_size = 64
        # Could implement some random transforms here so it's not always in the center, but not important for my use case.

        img = img.convert('RGBA').resize((x_size, y_size))
    
        # Turn mask image black but retain alpha channel
        img_np = np.array(img)
        mask = np.zeros_like(img_np)
        mask[..., -1] = img_np[..., -1]
        mask = Image.fromarray(mask)

        # Generate images of either white or random noise
        white = Image.fromarray(np.full((x_size, y_size),255)).convert('RGBA')
        noise = Image.fromarray(np.random.randint(0,255, size=(x_size, y_size))).convert('RGBA')

        # Concat using the alpha channel as a mask
        # We can now change to grayscale as we don't need the alpha channel
        white_img = Image.alpha_composite(white, mask).convert('L')
        noise_img = Image.alpha_composite(noise, img).convert('L')

        # Save images
        white_img.save(f'{dir_mask}\\{file}')
        noise_img.save(f'{dir_noise}\\{file}')


if __name__ == '__main__':
    main(working)