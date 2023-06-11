from rest_framework import serializers
from logistic.models import Product, StockProduct, Stock

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title', 'description']

class ProductPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)

        for position in positions:
            stock_product = StockProduct.objects.create(stock=stock, product=position['product'], quantity=position['quantity'], price=position['price'])

        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)

        for product in positions:
            stock_product = StockProduct.objects.update_or_create(stock=stock, product=product['product'], defaults={'quantity': product['quantity'], 'price': product['price']})
        return stock
