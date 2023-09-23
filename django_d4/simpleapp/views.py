# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)
from .models import Product
# -----------------
from django.http import HttpResponse
from .filters import ProductFilter
from django.urls import reverse_lazy
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class ProductsList(ListView):
    # Указываем модель объекты которой будем выводить

    model = Product

    # Поле, которое будет использоваться для сортировки объектов

    ordering = 'name'

    # queryset = Product.objects.filter(
    #     price__lt=900
    # ).order_by('-name')

    # Указываем имя шаблона, в котором будут все инструкции о том, как именно
    # пользователю должны быть показаны наши объекты

    template_name = 'products.html'  # шаблон, который будет использоваться

    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.

    context_object_name = 'products'  # Переменная в шаблоне в которую
    # передаётся вся информация из модели

    # Метод get_context_data позволяет изменить набор данных,
    # который будет передан в шаблон
    paginate_by = 5  # вот так можно указать количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # получаем обычный запрос
        queryset = super().get_queryset()
        # используем наш класс фильтрации
        # self.request.GET содержит объект QueryDict, который рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса, чтобы потом добавить в
        # контекст и использовать в шаблоне
        self.filterset = ProductFilter(self.request.GET, queryset)
        # возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        # С помощью super() обращаемся к родительским классам и вызываем у них
        # метод get_context_data с теми же аргументами.
        # В ответе должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'
        # context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['filterset'] = self.filterset

        # context['next_sale'] = "Распродажа в среду!"

        return context


def multiply(request):
    number = request.GET.get('number')
    multiplier = request.GET.get('multiplier')

    try:
        result = int(number) * int(multiplier)
        html = f"<html><body><h1>{number}*{multiplier}={result}</h1></body></html>"
    except (ValueError, TypeError):
        html = f"<html><body><h1>Invalid input.</h1></body></html>"

    return HttpResponse(html)


class ProductDetail(DetailView):
    # Модель всё та же, но мы хотим получить информацию по отдельному товару
    model = Product
    # Используем другой шаблон product.html
    template_name = 'product.html'
    # Название в котором будет выбранный пользователем продукт
    context_object_name = 'product'


class ProductsForm(ListView):
    model = Product
    ordering = 'name'
    template_name = 'products_form.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


# Добавляем новое представление для создания товаров.
class ProductCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    # Указываем нашу разработанную форму
    form_class = ProductForm
    # модель товаров
    model = Product
    # и новый шаблон, в котором используется форма
    template_name = 'product_edit.html'


# Добавляем представление для изменения товара.
class ProductUpdate(UpdateView):
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'


# Представление удаляющее товар.
class ProductDelete(DeleteView):
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')

# @login_required
# def show_protected_page(request):
#     // do something protected
