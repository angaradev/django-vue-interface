from product.models import Product, ProductRating
import random


def insert_rating():
    products = Product.objects.all()
    count = 0
    new_count = 0
    for product in products:
        try:
            rating = product.product_rating.first()
            if rating.product.count == 0 or rating.score == 0 or rating.quantity == 0:

                rating.score = random.randint(3, 5)
                rating.quantity = random.randint(1, 20)
                rating.save()
                count += 1
        except:
            rating = ProductRating(
                product=product,
                score=random.randint(3, 5),
                quantity=random.randint(1, 20),
            )
            new_count += 1

    print("Product ratings updated: ", count, "New product", new_count)
