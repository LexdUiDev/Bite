from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from .models import Restaurant, MenuItem, Order
from rest_framework.decorators import action
from .serializers import RestaurantSerializer, MenuItemSerializer, OrderSerializer


# Create your views here.

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Restaurant.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)




class MenuItemViewSet(viewsets.ModelViewSet):
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return MenuItem.objects.filter(restaurant__owner=self.request.user)


    def perform_create(self, serializer):
        restaurant = serializer.validated_data['restaurant']
        if restaurant.owner != self.request.user:
            raise PermissionError("You can't add items to this restaurant")
        serializer.save()


    def perform_update(self, serializer):
        menu_item = self.get_object()
        if menu_item.restaurant.owner != self.request.user:
            raise PermissionError("You can't edit this item")
        serializer.save()


    def perform_destroy(self, instance):
        if instance.restaurant.owner != self.request.user:
            raise PermissionError("You can't delete this item")
        instance.delete()




class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
       



    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAdminUser])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=400)
        order.status = new_status
        order.save()
        return Response({'status': order.status})