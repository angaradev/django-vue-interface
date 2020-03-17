from rest_framework import serializers
from product.models import (Product, ProductImage,
                            Category, Units, CarModel, CarMake, CarEngine)
from brands.models import BrandsDict


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class UnitsSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(model_field=Units()._meta.get_field('id'))

    class Meta:
        model = Units
        fields = ('id', 'unit_name')


class CarMakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMake
        fields = '__all__'


class CarModelSerializer(serializers.ModelSerializer):
    carmake = CarMakeSerializer(
        instance=CarMake, required=False, read_only=True)

    class Meta:
        model = CarModel
        fields = '__all__'


class CarEngineSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarEngine
        fields = '__all__'


class BrandsDictSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(model_field=BrandsDict()._meta.get_field('id'))

    class Meta:
        model = BrandsDict
        fields = ('id', 'brand')


class ProductSerializer(serializers.ModelSerializer):
    #unit = UnitsSerializer(instance=Units)
    car_model = CarModelSerializer(instance=CarModel, required=False)
    engine = CarEngineSerializer()

    class Meta:
        model = Product
        #fields = '__all__'
        fields = ['id',
                  'name',
                  'cat_number',
                  # 'created_date',
                  # 'updated_date',
                  'slug',
                  'brand',
                  'car_model',
                  'unit',
                  'one_c_id',
                  'active',
                  'engine'
                  ]

        # represent full fields of serializer nested objects
        depth = 0

    # Create method
    def create(self, validated_data):
        category_data = validated_data.pop('category')
        related_data = validated_data.pop('related')

        related_ids = [x.id for x in related_data]
        product = Product.objects.create(**validated_data)

        # Here we are creating Many To Many Fields for Category and ProductRelated
        categories = Category.objects.filter(name__in=category_data)
        for category in categories:
            product.category.add(category)
        related_porducts = Product.objects.filter(id__in=related_ids)
        for prod in related_porducts:
            product.related.add(prod)
        return product

    def update(self, instance, validated_data):

        # Менее Адский гемор по вложенной сериализации
        unit_data = validated_data.pop('unit')
        try:
            unit_qs = Units.objects.get(id=unit_data.id)
            instance.unit = unit_qs
        except:
            pass

        # Brand updating logic
        # print(validated_data.get('brand').id)
        # brand_data = validated_data.pop('brand')

        try:
            brand_qs = BrandsDict.objects.get(
                id=validated_data.get('brand').id)
            instance.brand = brand_qs
        except:
            pass

        instance.brand = validated_data.get('brand', instance.brand)
        instance.name = validated_data.get('name', instance.name)
        instance.cat_number = validated_data.get(
            'cat_number', instance.cat_number)
        instance.slug = validated_data.get('slug', instance.slug)
        # instance.car_model = validated_data.get(
        #    'car_model', instance.car_model)
        instance.one_c_id = validated_data.get('one_c_id', instance.one_c_id)
        instance.active = validated_data.get('active', instance.active)
        instance.save()

        return instance
