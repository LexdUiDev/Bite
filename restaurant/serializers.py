from rest_framework import serializers
from .models import Restaurant, MenuItem, Order

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'owner', 'name', 'description', 'address', 'phone_number', 'created_at']
        read_only_fields = ['id', 'owner', 'created_at']




class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
        image = serializers.ImageField(use_url=True)





class OrderSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)
    item_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=MenuItem.objects.all(),
        write_only=True,
        source='items'
    )
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'restaurant', 'items', 'status','item_ids', 'created_at', 'updated_at']
        read_only_fields = ['status', 'created_at', 'updated_at']