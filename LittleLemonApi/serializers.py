from rest_framework import serializers
from decimal import Decimal
from .models import MenuItem, Category, Rating
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class MenuItemSerializer(serializers.ModelSerializer):
	stock = serializers.IntegerField(source='inventory')
	price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
	category_id = serializers.IntegerField(write_only=True)
	category = CategorySerializer(read_only=True)
	price = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=1)

	class Meta:
		model = MenuItem
		fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category', 'category_id']

	def calculate_tax(self, product: MenuItem):
		return product.price * Decimal(1.1)

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
		queryset = User.objects.all(),
		default = serializers.CurrentUserDefault()
	)
    class Meta:
        model = Rating
        fields = ['user', 'menuitem_id', 'rating']
        
        validators = [
			UniqueTogetherValidator(
				queryset=Rating.objects.all(),
				fields = ['user', 'menuitem_id']
			)
		]
        
        extra_kwargs = {
			'rating': {'min_value': 0, 'max_value': 5}
		}