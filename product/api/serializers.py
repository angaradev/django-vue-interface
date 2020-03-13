from rest_framework import serializers
from product.models import Product, ProductImage, Category


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    #product_image = ImageSerializer(many=True)
    class Meta:
        model = Product
        #fields = '__all__'
        fields = ['id',
                  'name',
                  'cat_number',
                  'created_date',
                  'updated_date',
                  'slug',
                  'brand',
                  'car_model',
                  'unit',
                  'category',
                  'related',
                  #'product_image'
                  ]

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        related_data = validated_data.pop('related')
        
        related_ids = [x.id for x in related_data]
        product = Product.objects.create(**validated_data)
        
        #Here we are creating Many To Many Fields for Category and ProductRelated
        categories = Category.objects.filter(name__in=category_data)
        for category in categories:
            product.category.add(category)
        related_porducts = Product.objects.filter(id__in=related_ids)
        for prod in related_porducts:
            product.related.add(prod)
        
        return product