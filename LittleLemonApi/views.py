from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import MenuItem, Category, Rating
from .serializers import MenuItemSerializer, CategorySerializer
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import RatingSerializer



@api_view(['GET', 'POST'])
def menu_items(request):
    if(request.method == 'GET'):
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get("to_price")
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default = 2)
        page = request.query_params.get('page', default = 1)
        if category_name:
            items = items.filter(category__title = category_name)
        if to_price:
            items = items.filter(price__lte = to_price)
        if search:
            items = items.filter(title__startswith = search)
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)
        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []
        serialized_data = MenuItemSerializer(items, many=True)
        return Response(serialized_data.data)
    elif request.method == 'POST':
        serialized_item = MenuItemSerializer(data = request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item._validated_data, status=status.HTTP_201_CREATED)
    
    
@api_view()
def single_item(request, id):
    item = get_object_or_404(MenuItem, pk=id)
    serialized_item = MenuItemSerializer(item)
    return Response(serialized_item.data)



@api_view
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name="Manager").exist():
        return Response({"message": "Only manager should see this"})
    else:
        return Response({"message": "You are not authorized"}, 403)
    
    
    
class RatingsView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    
    def get_permissions(self):
        if(self.request.method == 'GET'):
            return []
        return [IsAuthenticated]
        
    