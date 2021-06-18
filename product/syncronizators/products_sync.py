from datetime import datetime
from django.conf import ONE_C_PRICE
from product.models import Product, CarModel, Stock, Store
from brands.models import BrandsDict
import csv


start = datetime.now()
car_model_list = {
    "Sonata": ["sonata"],
    "Elantra": ["elantra"],
    "Santa Fe": ["santafe"],
    "Porter2": ["porter2"],
    "Porter": ["porter1"],
    "Istana": ["istana"],
    "Solaris": ["solaris"],
    "Bongo": ["bongo3"],
    "Starex": ["starex"],
    "Grace": ["grace"],
    "Spectra": ["spectra"],
    "Tucson": ["tukson"],
    "Accent": ["accent"],
    "HD": ["hd65", "hd72", "hd78"],
    "Rio": ["rio"],
    "COROLLA": ["corolla"],
    "Ducato": ["ducato"],
    "TRANSIT": ["tranzit"],
    "LOGAN": ["logan"],
    "L200": ["l200"],
    "Peugeot boxer": ["bokser"],
    "Sportage": ["sportage"],
    "IX35": ["ix35"],
    "Aero tawn": ["aerotaun"],
    "FOCUS": ["fokus"],
    "JUMPER": ["dzhamper"],
    "Cerato": ["serato"],
    "Besta": ["besta"],
    "Trajet": ["tradzhet"],
    "Sorento": ["sorento"],
    "Ceed": ["ceed"],
    "Terracan": ["terakan"],
    "Pregio": ["pajero"],
    "Soul": ["soul"],
    "Tourneo connect": ["tourneo-connect"],
    "Carnival": ["carnival"],
}
# Bring dict keys to lowercase
lower_cars = {}
for key, value in car_model_list.items():
    lower_cars[key.lower()] = value

f = 0
csv_ids = []

with open(ONE_C_PRICE) as file:
    reader = csv.reader(file, delimiter=";")
    csv_list = list(reader)


csv_dict = []
i = 0
for product in csv_list:
    try:
        csv_ids.append(int(product[2]))
        csv_dict.append(
            {
                "name": product[0],
                "one_c_id": int(product[2]),
                "brand": product[10] if product[9] else "origin",
                "car_model": product[8].lower(),
                "cat_number": product[3],
                "price": float(product[7]) if product[7] else 0,
                "quantity": int(product[1]) if product[1] else 0,
                "availability_days": 0,
            }
        )
    except:
        i += 1


products = Product.objects.all()
product_id_list = [x.one_c_id for x in products]
print("Lenght of product id list is:", len(product_id_list))
update_list = []
create_list = []
obj_create_list = []
i = 0
j = 0
for csv_prod in csv_dict:
    brand = None
    car_model = None
    try:
        brand = BrandsDict.objects.get(brand=csv_prod["brand"])
    except:
        pass
    #     try:
    #         car_model = CarModel.objects.get(slug=csv_prod['car_model'])
    #         car_model_list = cars[csv_prod['car_model']]
    #     except:
    #         pass

    if csv_prod["one_c_id"] in product_id_list:
        # update product herer
        i += 1
        update_list.append(csv_prod)
        django_product = Product.objects.get(one_c_id=csv_prod["one_c_id"])
        try:
            stock = Stock.objects.get(product=django_product, store=1)
            stock.price = csv_prod["price"]
            stock.quantity = csv_prod["quantity"]
            stock.save()
        except:
            new_stock = Stock(
                product=django_product,
                store=Store.objects.get(id=1),
                price=csv_prod["price"],
                quantity=csv_prod["quantity"],
            )
            new_stock.save()
    else:
        # create product here
        j += 1
        create_list.append(csv_prod)

        new_product = Product(
            name=csv_prod["name"],
            brand=brand,
            one_c_id=csv_prod["one_c_id"],
            cat_number=csv_prod["cat_number"],
        )
        new_product.save()
        try:
            for car in lower_cars[csv_prod["car_model"].lower()]:
                try:
                    car_model = CarModel.objects.get(slug=car.lower())
                    new_product.car_model.add(car_model)
                except:
                    f += 1
        except:
            pass
        st = Stock(
            product=new_product,
            store=Store.objects.get(id=1),
            price=csv_prod["price"],
            quantity=csv_prod["quantity"],
        )
        st.save()


end = datetime.now()
print(end - start)
print(i, j)
print(update_list[:1])
print("-------------------" * 6)
print(obj_create_list[:1])
print(f, "Fuck up count")
