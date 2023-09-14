from django.urls import path
from .views import ProductsList, ProductDetail, ProductsForm


urlpatterns = [
    # path - означает ПУТЬ
    # В данном случае путь ко всем товарам останется пустым
    # Т.к. объявленное представление является классом, а Django ожидает
    # функцию, надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('', ProductsList.as_view()),
    # pk - это первичный ключ товара, который будет выводиться у нас в шаблон
    # int - указывает на то, что принимаются только целочисленные значения
    path('<int:pk>', ProductDetail.as_view()),
    path('products_form/', ProductsForm.as_view()),

]