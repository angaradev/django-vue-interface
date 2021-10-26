from product.models import Category, CategoryYandexMarket
from django.conf import settings
import csv, pathlib, os


def yand_cats_insert_update():
    cwd = pathlib.Path().cwd()
    file_path = os.path.join(settings.BASE_DIR, "product/syncronizators/cats.csv")

    all_cats = Category.objects.all()
    created_count = []

    with open(file_path, "r") as r_file:
        reader = csv.reader(r_file, delimiter=",")
        for row in reader:
            yand_name = row[2].split("/")[-1]
            try:
                shop_cat_id = row[1]
                cat = all_cats.get(id=shop_cat_id)
                yand_cat, created = CategoryYandexMarket.objects.update_or_create(
                    shop_cat=cat, name=yand_name
                )

                created_count.append(created)
            except Exception as e:
                print("Something goes wrong", e)

        print("Created :", len(created_count))
