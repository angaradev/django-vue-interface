

import csv
from django.db.models import Avg, Count
from product.models import Stock
from product.models import Product
import os



home_directory = os.path.expanduser( '~' )







def make_list_for_anton():
    stocks = Stock.objects.filter(quantity__gt=0)
    print(stocks.count())
    items = []
    def cats(cat):
        ret = ''
        try:
            ret = '|'.join([x.name for x in cat.get_family()])
        except:
            ret = ''
        return ret
            
    with open('list.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='"')
        writer.writerow(['one_c_id', 'name', 'make', 'model','category', 'brand', 'price', 'quantity', 'cat_number'])

        for stock in stocks:
            
            item =[ stock.product.one_c_id, stock.product.name,\
                    "|".join([x.carmake.name for x in stock.product.car_model.all()]),\
                    "|".join([x.name for x in stock.product.car_model.all()]),\
                   cats(stock.product.category.first()),\
                    str(stock.product.brand), str(stock.price), stock.quantity, \
                    stock.product.cat_number
                  ]
            #writer.writerow(item)
            items.append(item)
            writer.writerow(item)
