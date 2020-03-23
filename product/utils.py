from django.utils.text import slugify
from transliterate import translit
from langdetect import detect
import re
import os
from PIL import Image, ImageOps

# Slugifyer for products


def unique_slug_generator(instance, name, slug_field):

    if detect(name) == 'ru':
        slug = slugify(translit(name, 'ru', reversed=True))
    else:
        slug = slugify(name)

    model_class = instance.__class__

    while model_class._default_manager.filter(slug=slug).exists():
        object_pk = model_class._default_manager.latest('pk')
        object_pk = str(object_pk.id + 1)

        slug = f'{slug}-{object_pk}'
    return slug


def get_youtube_id(url):  # Getting youtube video ID form url
    myregexp = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})'
    regexp = re.compile(myregexp)
    m = regexp.search(url)
    return m.group(1)

##########################################################
# This function uses nowhere but exist as an example for resizing by PIL


def image_resizer(img, size):  # Image resizer for saving to bd different sizes
    file = 'tai.jpg'
    im = Image.open(file)
    file, ext = os.path.splitext(file)
    im = ImageOps.fit(im, size, method=Image.NEAREST,
                      bleed=0.0, centering=(0.5, 0.5))

    im.save("thumbnail" + file + ext)


# File deletedef
def delete_file(path):  # Deleting Files from disk
    if os.path.isfile(path):
        os.remove(path)
