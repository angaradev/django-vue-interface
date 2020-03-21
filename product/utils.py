from django.utils.text import slugify
from transliterate import translit
from langdetect import detect


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
