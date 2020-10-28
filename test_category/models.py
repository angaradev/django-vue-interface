from django.db import models
from django.db.models.signals import pre_save
from product.utils import unique_slug_generator

# Create your models here.
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField


class Categories(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        db_index=True,
        on_delete=models.DO_NOTHING,
    )
    slug = models.SlugField(blank=True)

    class Meta:
        verbose_name = "Категории"

    def __str__(self):
        return self.name

    @property
    def type(self):
        return "shop"

    @property
    def items(self):
        return 123

    @property
    def layout(self):
        return "products"


def category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, instance.name, instance.slug)


pre_save.connect(category_slug, Categories)
