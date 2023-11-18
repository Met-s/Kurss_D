                                                       Зарегистрировал модели

simpleapp/admin.py

from django.contrib import admin
from .models import Category, Product

admin.site.register(Category)
admin.site.register(Product)
----------------------------------
В данный момент нам нужен дженерик ListView, который выводит список объектов
модели, используя указанный шаблон.

simpleapp/views.py

# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView
from .models import Product

class ProductsList(ListView):
    # Указываем модель объекты которой будем выводить
    model = Product
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'name'
    # Указываем имя шаблона, в котором будут все инструкции о том, как именно
    # пользователю должны быть показаны наши объекты
    template_name = 'products.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'products'

Вот так можно использовать дженерик ListView для вывода списка товаров:
 1.Создаём свой класс, который наследуется от ListView
 2.Указываем модель, из которой будем выводить данные.
 3.Указываем поле сортировки данных модели (необязательно)
 4.Записываем название шаблона.
 5.Объявляем, как хотим назвать переменную в шаблоне.
-------------------------------
                                                            Настраиваем адрес:
Для этого необходимо настроить пути в файле urls.py. При выполнении
инициализации нового приложения Django не создавал этот файл в нашей директории,
поэтому мы создадим его сами.
simpleapp/urls.py

from django.urls import path
from .views import ProductsList

urlpatterns = [
    # path - означает ПУТЬ
    # В данном случае путь ко всем товарам останется пустым
    # Т.к. объявленное представление является классом, а Django ожидает
    # функцию, надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('', ProductsList.as_view()),
]
Задали ПУТЬ к нашему представлению
-----------------------------------
Вывод из БД. Для этого в главном файле urls.py в котором подключали flatpages
нужно сделать так, чтобы он автоматически включал все наши адреса из приложения
 и добавлял к нему префикс products.

django_d3/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    # Делаем так, чтобы все адреса из нашего приложения (simpleapp/urls.py)
    # подключались к главному приложению с префиксом products/.
    path('products/', include('simpleapp.urls')),
]
------------------------------------
Настроил settings.py

'django.contrib.sites',
'django.contrib.flatpages',
'simpleapp'

SITE_ID = 1

'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

'DIRS': [os.path.join(BASE_DIR, 'templates')],
или
'DIRS': [BASE_DIR / 'templates'],

STATICFILES_DIRS = [
    BASE_DIR / "static"
]
---------------------------------------
Применил миграции

py manage.py makemigrations
py manage.py migrate

Создал супер юзера

py manage.py createsuperuser
---------------------------------------
Добавляем шаблон default.html

templates/flatpages/default.html
---------------------------------------
Добавил папку static и изменил шаблон в default.html
---------------------------------------
добавление панели в админке: для зарегистрированных пользователей
создадим файл django_d3/flatpages/admin.py

from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _

# Define a new FlatPageAdmin
class FlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
        'classes': ('collapse',),
        'fields': (
            'enable_comments',
            'registration_required',
            'template_name',
         ),
        }),
    )
# Re-register FlatPageAdmin
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

Нужно зарегистрировать новое приложение Flatpages в настройках settings.py
'fpages'
---------------------------------------
Несмотря на то, что мы видим довольно неказистый текст (пока что),всё же здесь
присутствуют наши товары.

Если переложить всё, что сделали на MVC, то получится:
1. Model - сделали модели для товаров и категорий в models.py
2. View - написали темплейт в products.html
3. Controller - настроили представление с логикой вывода списка товаров в views.py
Вот все части MVC и сложились в нашем приложении.
---------------------------------------
views.py
Фильтр цена ниже 500
class ProductsList(ListView):
    # Указываем модель объекты которой будем выводить
    # model = Product
    # Поле, которое будет использоваться для сортировки объектов
    # ordering = 'name'
    queryset = Product.objects.filter(
        price__lt=500
    )
    # Указываем имя шаблона, в котором будут все инструкции о том, как именно
    # пользователю должны быть показаны наши объекты
    template_name = 'products.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'products'
----
Можно добавить сортировку и по имени
queryset = Product.objects.filter(
        price__lt=900
    ).order_by('-name')
---------------------------------------
Добавил в views.py class ProductDetail(DetailView):
для отображения одного продукта
---------------------------------------
Добавляем адрес в simpleapp/urls.py.
Адрес будет немного отличаться. В него нужно добавить идентификатор товара,
который хотим получить.
    # pk - это первичный ключ товара, который будет выводиться у нас в шаблон
    # int - указывает на то, что принимаются только целочисленные значения
path('<int:pk>', ProductDetail.as_view()),
---------------------------------------
Добавляем новый шаблон для вывода одного товара по id
django_d3/templates/product.html
---------------------------------------
Подытожим
1. Добавил новое представление в view.py
2. Зарегистрировал представление в urls.py на путь, который содержит
    целочисленный идентификатор объекта.
3. Добавил новый шаблон в templates для представления.
---------------------------------------------------------
Изменил templates/products.html добавил условие если товаров нет, выводится
сообщение Товаров нет!
{% block content %}
    <hr>
    <h3>products.html</h3>
    <hr>
    <h1>Все товары</h1>
        {% if products %}
            {{ products }}
        {% else %}
            <h2>Товаров нет!</h2>
        {% endif %}
{% endblock content %}
---------------------------------------
Это обычное условие из python:
В шаблонах выглядит так:

{% if <условие> %} # Блок HTML кода, который отобразится если условие истинно

{% elif <условие 2> %} # Блок HTML кода, который отобразится если условие 2 истинно

{% else %} # Блок HTML кода, который отобразится только если оба условия ложны

{% endif %}
---------------------------------------
Изменил templates/products.html
Создал таблицу:
{% block content %}
    <hr>
    <h3>products.html</h3>
    <hr>
    <h1>Все товары</h1>
        {% if products %}
            <table>
                <tr>
                    <td>Название</td>
                    <td>Описание</td>
                    <td>Категория</td>
                    <td>Цена</td>
                    <td>Количество</td>
                </tr>
            </table>
        {% else %}
            <h2>Товаров нет!</h2>
        {% endif %}
{% endblock content %}
---------------------------------------
Заполнил таблицу
{% block content %}
    <hr>
    <h3>products.html</h3>
    <hr>
    <h1>Все товары</h1>
        {% if products %}
            <table>
                 <tr>
                    <td>Название</td>
                    <td>Описание</td>
                    <td>Категория</td>
                    <td>Цена</td>
                    <td>Количество</td>
                </tr>
                {% for product in products %}
                <tr>
                    <td>{{ product.name }}</td>
                    <td>{{ product.description }}</td>
                    <td>{{ product.category.name }}</td>
                    <td>{{ product.price }}</td>
                    <td>{{ product.quantity }}</td>
                </tr>
                {% endfor %}
            </table>
        {% else %}
            <h2>Товаров нет!</h2>
        {% endif %}
{% endblock content %}
---------------------------------------
Фильтр в шаблоне: отрезает 15 символов и добавляет ...
<tr>
    <td>{{ product.name }}</td>
    <td>{{ product.description|truncatechars:15 }}</td>
    <td>{{ product.category.name }}</td>
    <td>{{ product.price }}</td>
    <td>{{ product.quantity }}</td>
</tr>
---------------------------------------
Фильтр в шаблоне: отрезает 2 слова и добавляет ...
<td>{{ product.description|truncatewords:2 }}</td>

Фильтры очень похожи на методы или функции и имеют примерно следующий синтаксис:
<переменная>|<название метода>:<аргументы>
---------------------------------------
1. Импортировал модуль datetime, чтобы получить текущую дату
2. Переопределил метод get_context_data, добавив две переменные, которые будут
доступны в шаблоне.

from datetime import datetime
class ProductsList(ListView):
# Метод get_context_data позволяет изменить набор данных,
    # который будет передан в шаблон

    def get_context_data(self, **kwargs):
        # С помощью super() обращаемся к родительским классам и вызываем у них
        # метод get_context_data с теми же аргументами.
        # В ответе должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = None
        return context
---------------------------------------
Добавил отображение пользователю

{% block content %}
    <hr>
    <h3>products.html</h3>
    <hr>
    <h1>Все товары</h1>

    # Используем переданную из представления переменную time_now и применяем
    к ней фильтр data. По назначению этот фильтр очень похож на метод
    strftime у объекта datetime в Python - вывод времени в указанном формате.

    <h3>{{ time_now|date:'M d Y'}}</h3>
    <hr>
        {% if products %}
            <table>
                 <tr>
                    <td>Название</td>
                    <td>Описание</td>
                    <td>Категория</td>
                    <td>Цена</td>
                    <td>Количество</td>
                </tr>
                {% for product in products %}
                <tr>
                    <td>{{ product.name }}</td>
                    <td>{{ product.description|truncatewords:2 }}</td>
                    <td>{{ product.category.name }}</td>
                    <td>{{ product.price }}</td>
                    <td>{{ product.quantity }}</td>
                </tr>
                {% endfor %}
            </table>
        {% else %}
            <h2>Товаров нет!</h2>
        {% endif %}
{% endblock content %}
---------------------------------------
Сообщение о распродаже:  next_sale взята из
def get_context_data(self, **kwargs): файла views.py

products.html

{% block content %}
    <hr>
    <h3>products.html</h3>
    <hr>
    <h1>Все товары</h1>
    <h3>{{ time_now|date:'M d Y'}}</h3>
<!--        Если в переменной next_sale будет NONE,
то выведется указанный в переменной текст-->
        <h3> {{ next_sale|default_if_none:"Чуть позже сообщим о распродаже!" }}</h3>
    <hr>
        {% if products %}
---------------------------------------
При замене значения next_sale в представлении views.py на какую-нибудь строку,
будет выведено её содержимое.

def get_context_data(self, **kwargs):
        # С помощью super() обращаемся к родительским классам и вызываем у них
        # метод get_context_data с теми же аргументами.
        # В ответе должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.

        context['next_sale'] = "Распродажа в среду!"

        return context
----------------
Обратите внимание, что тег default_if_none не обрабатывает пустые строки,
пустые списки и прочее. Его задача отследить только переменную None.
Для того чтобы отлавливать пустые строки, списки и другое, используется фильтр
 default, который имеет точно такой синтаксис.
---------------------------------------
                                                            Собственный фильтр

from django import template

register = template.Library()

# Регистрируем фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблона, а не простая функция.

@register.filter()
def currency(value):
    """
    value: значение, к которому нуо применить фильтр
    """
    # Возвращаемое функцией значение подставится в шаблон.
    return f'{value} P'
-----------------
Декоратор register.filter() указывает Django, что нужно запомнить про
существование нового фильтра. Название фильтра по умолчанию берётся равным
названию функции,то есть в шаблоне можно писать  {{ price|currency }}.
Можно самим назвать фильтр. Например: register.filter(name='currency_rub'),
а название функции не менять, тогда в шаблоне пишем {{ price|currency_rub }}.
-------------------
Функция, которую зарегистрировали как фильтр, очень простая. Она принимает один
аргумент - переменную, с которой его используют в шаблоне. Сама функция
выполняет просто форматирование строки и сразу её возвращает. Результат этой
функции и будет подставлен в шаблоне.
----------------
После добавления файла с новыми фильтрами, нужно перезагрузить Django-сервер.
----------------
Просто взять и указать фильтр в шаблоне не получится.
Нужно подключить свои фильтры в шаблоне.
Сделать это можно с помощью указания тега {% load custom_filters %}
Где custom_filters - это название файла с нашим фильтром.
---------------------------------------
Добавили словарь со списком кодов валют и их символов, используем в функции.
Мы не увидим, ни каких ошибок насчёт того, что аргумент у фильтра есть, а мы
его не используем. Потому что указали значение по умолчанию code='rub'.

CURRENCIES_SYMBOLS = {
    'rub': 'руб',
    'usd': '$',
}

@register.filter()
def currency(value, code='rub'):
    """
    value: значение, к которому нуо применить фильтр

    """
    postfix = CURRENCIES_SYMBOLS[code]
    # Возвращаемое функцией значение подставится в шаблон.
    return f'{value} {postfix}'
---------------
Укажем в шаблоне products.html "usd"

<tr>
    <td>{{ product.name }}</td>
    <td>{{ product.description|truncatewords:2 }}</td>
    <td>{{ product.category.name }}</td>
    <td>{{ product.price|currency:"usd" }}</td>
    <td>{{ product.quantity }}</td>
</tr>
---------------------------------------
Теперь разберёмся с тегами.
Представим что текущую дату нужно вывести на множестве страниц.

simpleapp/templatetags/custom_tags.py

from datetime import datetime
from django import template

register = template.Library()

@register.simple_tag()
def current_time(format_string='%b %d %Y'):
    return datetime.utcnow().strftime(format_string)
-------------------
products.html

{% extends 'flatpages/default.html' %}
{% load custom_filters %}
<!--Подключаем новый файл с нашим тегом-->
{% load custom_tags %}

<h2>{% block title %}
    Products
    {% endblock title %}}</h2>

{% block content %}
    <hr>
    <h3>products.html</h3>
    <hr>
    <h1>Все товары</h1>
<!--Вот так выглядело использование переменной и фильтра-->
<!--    <h3>{{ time_now|date:'M d Y'}}</h3>-->

<!--А вот так мы используем наш тег-->
    <h3>{% current_time '%b %d %Y' %}</h3>


<!--        Если в переменной next_sale будет NONE,
то выведется указанный в переменной текст-->
        <h3> {{ next_sale|default_if_none:"Чуть позже сообщим о распродаже!" }}</h3>
    <hr>
        {% if products %}
-------------------
А вот от переменной time_now, которую мы указали в представлении, теперь можно
избавиться и переиспользовать наш тег в любых шаблонах. Также как и для фильтра,
указали значение аргумента по умолчанию. Делать это необязательно, но если в
большинстве случаев будет использоваться одно и тоже значение аргумента,
то проще указать его по умолчанию.
---------------------------------------
Метод pprint:
views.py

from pprint import pprint

 def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next_sale'] = "Распродажа в среду!"

        pprint(context)

        return context
Перезапускаем страницу и можем посмотреть в терминале что хранится
в переменной context

 pprint(id(context['object_list']))
=======================================
=======================================
Django_D4_Начало                                              Django_D4_Начало
=======================================
GET запрос                                                          GET запрос
!!!!!!!!!!!!!!!
GET запрос - это HTTP- запрос в котором описано, что использован метод GET.
Например: браузер посылает HTTP- запрос с таким методом во время открытия
любого сайта для того, чтобы получить HTML-код и отрендерить его пользователю.

Кроме получения данных мы можем также создавать, изменять и удалять их.
Для этого стараются использовать другие методы - POST,DELETE и другие.
Для этого возьмём ссылку:
https://docs.djangoproject.com/en/4.0/search/?q=reqest&page=2
и разложим её на составляющие:

https - схема
:// - последовательность, которая отделяет схему от домена
docs.djangoproject.com - домен(вместо него может быть указан ip адрес)
/en/4.0/search/ - путь к ресурсу
? - знак, который отделяет параметры от ресурса
q=request&page=2 - параметры запроса (на английском указывают как -
                    query string или query parameters)

Нас интересуют параметры запроса. Через них можно указать номер страницы или
фильтрацию. При этом пользователь может скопировать текущий URL открытой страницы
и отправить его кому-нибудь. Так как параметр запроса хранился в URL, при
следующем открытии пользователь получит те же данные, что видел в последний раз.
Это если не было никаких изменений в БД или приложении.

Посмотрим на Пример:
https://docs.djangoproject.com/en/4.0/search/?q=reqest&page=2

В примере есть два параметра запроса с ключами q и page.
Ключ отделяется от значения знаком ( = ), а пары ключей значений - с помощью
амперсанда ( & ). Когда такой запрос поступает в Django, он раскладывает
параметры в объект класса QueryDict, который похож на Python словарь.
Главное отличие в том, что для одного ключа может быть несколько значений,
которые объединятся с списком.
>> QueryDict('a=1')  # запрос с параметром ?a=1
<QueryDit: {'a': ['1']}>
>> QueryDict('a=1&a=2&c=3')  # запрос с параметрами ?a=1&a=2&c=3
<QueryDit: {'a': ['1', '2'], 'c': ['3']}>
Этот объект, похожий на словарь, можно получить из объекта запроса, который
доступен в view.
-----------
Для примера напишем функциональную view, которая будет перемножать два переданных
числа, а если передадут не числа то выведет ошибку.
views.py функцию пишем в не класса

from django.http import HttpResponse

def multiply(request):
    number = request.GET.get('number')
    multiplier = request.GET.get('multiplier')

    try:
        result = int(number) * int(multiplier)
        html = f"<html><body>{number}*{multiplier}={result}</body></html>"
    except (ValueError, TypeError):
        html = f"<html><body>Invalid input.</body></html>"

    return HttpResponse(html)
---------------
Регистрируем view в urls.py В ОСНОВНОЙ

from django.contrib import admin
from django.urls import path, include
from simpleapp.views import multiply

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    # Делаем так, чтобы все адреса из нашего приложения (simpleapp/urls.py)
    # подключались к главному приложению с префиксом products/.
    path('products/', include('simpleapp.urls')),
    path('multiply/', multiply),

]
--------------
Посмотрим как работают параметры GET запроса.
Откроем страницу без указания параметров. Переменные number и multiplier
будут равны None, так как их нет в словаре request.GET. При переводе к int
произойдёт TypeError.

http://127.0.0.1:8000/multiply/
# Invalid input.
---------------
Передадим значения:
http://127.0.0.1:8000/multiply/?number=3&multiplier=2
# 3*2=6
---------------
Помимо словаря с параметрами GET-запроса в объекте request есть множество
других данных: тело POST-запроса, cookie, текущий пользователь и многое другое.
Почитать здесь:
https://docs.djangoproject.com/en/4.2/ref/request-response/
---------------------------------------
Пагинация                                                           Пагинация
!!!!!!!!!!!!!!!!!!!!!!!!!!
Пагинация - постраничный вывод информации на сайте.
Так как в urls.py мы регистрируем пути и view, нам не нужно прописывать
обработчик отдельно для каждой страницы. Укажем один путь а внутри view будем
смотреть, какую именно страницу или фильтрацию у нас запрашивает пользователь.
-------------
Добавим пагинацию.
views.py

class ProductsList(ListView):
    model = Product
    ordering = 'name'
    template_name = 'products.html'  # шаблон, который будет использоваться
    context_object_name = 'products'  # Переменная в шаблоне
    paginate_by = 2  # вот так можно указать количество записей на странице

------------
Запрос в браузере изменился
http://127.0.0.1:8000/products/?page=1
---------------------------------------
Добавим ссылки на другие страницы
templates/products.html

products.html

{% else %}
            <h2>Товаров нет!</h2>
        {% endif %}

Добавил вот этот код в шаблон:

        {# Добавим пагинацию на страницу #}
        {# Информация о предыдущих страницах #}
        {% if page_obj.has_previous %}
            <a href="?page=1">1</a>
            {% if page_obj.previous_page_number != 1 %}
            ...
            <a href="?page={{ page_obj.previous_page_number }}">{{ page_obj.previous_page_number }}</a>
            {% endif %}
        {% endif %}

        {# Информация о текущей странице #}
        {{ page_obj.number }}

        {# Информация о следующих страницах #}
        {% if page_obj.has_next %}
            <a href="?page={{ page_obj.next_page_number }}">{{ page_obj.next_page_number }}</a>
            {% if paginator.num_pages != page_obj.next_page_number %}
                ...
                <a href="?page={{ page_obj.paginator.num_pages }}">{{ page_obj.paginator.num_pages }}</a>
            {% endif %}
        {% endif %}


{% endblock content %}
-----------------------
Разберёмся, на каком объекте из контекста построен весь наш вывод товаров.

page_obj - это объект, в котором содержится информация о текущей странице.
            Сам он приходит из класса Paginator, который содержится в ListView.
В page_obj имеем доступ к переменным:

has_previous___________существует ли предыдущая страница
previous_page_number___номер предыдущей страницы
number_________________номер текущей страницы
has_next_______________существует ли следующая страница
next_page_number_______номер следующей страницы
paginator.num_pages____объект paginator содержит информацию о количестве страниц
                        в переменной num_pages
----------------
На основе этих переменных мы вывели ссылки на другие страницы списка товаров.
Ссылки создали с помощью HTML-тега ( а ), у которого в атрибуте ( href )
указали информацию о том, на какие параметры запроса (query string) нужно заменить
данные, используя текущий путь.
HTML - страница, которая будет отдаваться пользователю, будет содержать код
вида <a href=»?page=2»>2</a>/
Можно ещё прописать путь - <a href=»/products/?page=2»>2</a>
вместе с IP и портом - <a href="http://127.0.0.1:8000/products/?page=2"»>2</a>
Однако это не удобно если решим изменить путь до страницы с /products/ на /catalog/

Для решения текущей задачи нам достаточно изменить параметры запроса.
Между открывающимся тегом <a> и закрывающим </a> у нас указывается текст,
который виден на странице как ссылка.
В данном случае указываем номер страницы.
Подробнее здесь https://htmlbook.ru/html/a
Пагинация
https://docs.djangoproject.com/en/4.0/topics/pagination/
---------------------------------------
Фильтрация                                                          Фильтрация
!!!!!!!!!!!!!!!!!!!
Для фильтрации данных будем использовать -
сторонний Python пакет из PyPi - django-filter.
терминал

python -m pip install django-filter
Если будут трудности то нужно указать версию фильтра
python -m pip install django-filter==21.1
Подробно здесь https://pypi.org/project/django-filter/
--------------------
Добавим "django_filters" в settings.py/ INSTALLED_APPS чтобы получить доступ
к фильтрации в приложении.
--------------------
Создаём файл simpleapp/filters.py

from django_filters import FilterSet
from .models import Product
# Создаём набор фильтров для модели Product
# FilterSet, который наследуем очень похож на Django дженерики

class ProductFilter(FilterSet):
    class Meta:
        # В Meta классе нужно указать Django модель, в которой будем
        # фильтровать записи.
        model = Product
        # В fields описываем по каким полям модели будет
        # производиться фильтрация
        fields = {
            # Поиск по названию
            'name': ['icontains'],
            # Количество товаров должно быть больше или равно
            'quantity': ['gt'],
            'price': [
                'lt',  # цена меньше или равна указанной
                'gt',  # цена больше или равна указанной
            ],
        }
--------------------
В fields содержится словарь настройки самих фильтров.
Ключами являются названия полей модели, а значениями выступают списки операторов
фильтрации. Те которые мы указываем при составлении запроса.
Product.object.filter(price_gt=10).
Подробнее здесь
https://docs.djangoproject.com/en/4.0/ref/models/querysets/#field-lookups
--------------------
Теперь созданный класс нужно использовать в представлении view для фильтрации
списка товаров.
simpleapp/views.py

from .filters import ProductFilter

Добавляем функцию в
class ProductsList(ListView):


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
-------------------
Добавляем в HTML- поля для каждого фильтра, который объявили.
Для отправки набора информации со страницы в браузере в HTML существует
специальная сущность - форма.

Форма - это набор полей, которые пользователь может заполнить и отправить
в приложение на сервер.

Мы написали, что фильтровать товары можно по нескольким полям. Пользователь
может захотеть отфильтровать товары как по одному так и по всем полям сразу.
При этом наше приложение должно получить все фильтры за один раз. То есть,
например, запрос из браузера в наше приложение должен прийти с указанием
фильтра и по названию, и по стоимости в месте, а не отдельно. Для того чтобы
собрать все указанные пользователем данные и отправить их на сервер вместе,
нам и нужна форма. В HTML - форму задают с помощью тега <form>...</form>.
Внутри неё нужно указать заголовки и поля ввода данных. Также, помимо этого, в
форме зачастую присутствует кнопка для отправки данных на сервер.
------------------
Пример того как может выглядеть форма в HTML

<form>
    <label for="nameId">Name:</label>
    <input id="nameId" type="text" name="name">
    <input type="submit" value="Отправить">
</form>
------------------
Django-filter может сгенерировать за нас все поля ввода. Нам нужно только
использовать переменную, которую ы добавили в контекст (filterset), в шаблоне
и добавить кнопку отправки формы.

products.html

 {# Добавляем форму, которая объединяет набор полей, которые будут отправляться в запросе #}
    <form action="" method="get">
        {# Переменная которую передали через контекст, может сгенерировать нам форму с полями #}
        {{ filterset.form.as_p }}
        {# Добавим кнопку отправки данных формы #}
        <input type="submit" value="Найти" />
    </form>
-------------------
чтобы фильтрация не пропадала на других страницах

custom_tags.py

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()

Параметр декоратора takes_context=True сообщает Django, что для работы тега
требуется передать контекст.
Именно тот контекст который редактировали.
context['request'].GET.copy() нам позволяет скопировать все параметры текущего
запроса.
Далее по указанным полям устанавливаем новые значения, которые нам передали
при использовании тега.
В конце кодируем параметры в формат, который может быть указан в строке браузера.
Не каждый символ разрешается использовать в пути и параметрах запроса.
Подробнее здесь: https://en.wikipedia.org/wiki/Percent-encoding
-------------------
Тег сделали, осталось применить его в шаблоне.
Для этого добавим в ссылки пагинации.

products.html

{% endif %}
        {# Добавим пагинацию на страницу #}
        {# Информация о предыдущих страницах #}
        {% if page_obj.has_previous %}
            {# <a href="?page=1">1</a> # было #}

{# Для каждой ссылки пагинации указываем обработку через новый тег #}
  {# Стало #}
            <a href="?{% url_replace page=1 %}">1</a>

            {% if page_obj.previous_page_number != 1 %}
                ...
                {# Было  #}
            {# <a href="?page={{ page_obj.previous_page_number }}">{{ page_obj.previous_page_number }}</a> #}

  {# Стало #}
                <a href="?{% url_replace page=page_obj.previous_page_number %}">{{ page_obj.previous_page_number }}</a>

            {% endif %}
        {% endif %}

        {# Информация о текущей странице #}
        {{ page_obj.number }}

        {# Информация о следующих страницах #}
        {% if page_obj.has_next %}
            {# Было  #}
            {# <a href="?page={{ page_obj.next_page_number }}">{{ page_obj.next_page_number }}</a> #}

  {# Стало #}
            <a href="?{% url_replace page=page_obj.next_page_number %}">{{ page_obj.next_page_number }}</a>

            {% if paginator.num_pages != page_obj.next_page_number %}
                ...
                {# Было  #}
                {# <a href="?page={{ page_obj.paginator.num_pages }}">{{ page_obj.paginator.num_pages }}</a> #}

  {# Стало #}
                <a href="?{% url_replace page=page_obj.paginator.num_pages %}">{{ page_obj.paginator.num_pages }}</a>

            {% endif %}
        {% endif %}
{% endblock content %}
---------------------------------------
В данный момент в шаблонах использовали авто-генерацию HTML-кода формы.
Помимо этого, мы сами можем указать какие HTML-теги и их параметры должны
использоваться в форме.
Пример формы со строкой и кнопкой поиска.
Для этого создал файл products_form.htl  на основе products.html но изменил в
нём форму
<form action="" method="get">
        {{ filterset.form.non_field_errors }}
        {{ filterset.form.name__icontains.errors }}
        <label for="{{ filterset.form.name__icontains.id_for_label }}">Search</label>
        <input
            id="{{ filterset.form.name__icontains.id }}"
            name="{{ filterset.form.name__icontains.name }}"
            value="{{ filterset.form.name__icontains.value }}"
            class="form-control"
            >
        <input type="submit" class="mt-3 btn-primary" value="Найти" />
    </form>
----------------
Сначала с помощью {{ filterset.form.non_field_errors }} вывели все ошибки, не
относящиеся к полям формы.
После них пойдут ошибки, которые относятся к полю поиска по названию товара
{{ filterset.form.name__icontains.errors }}.
Далее составляем сами заголовки (label) и поля ввода данных формы (input).
В заголовках указываем для какого поля они создаются (атрибут for), а также
текст заголовка.
В поле ввода данных мы указываем больше информации:
id - идентификатор элемента, по которому заголовок будет связан с данным
полем;
name - значение, которое будет ключом поля при отправки данных на сервер.
    Ключ также можно увидеть в строке браузера слева от знака =.
    Например, в URL
    http://127.0.0.1:8000/products/products_form/?name__icontains=123
    часть name__icontains и является значением атрибута name.
value - значение, которое будет отправлено на сервер. Изначально мы заполняем его,
    чтобы после отправки запроса пользователем страница загрузилась без потери
    данных, указанных им в форме. Другими словами, если мы не будем заполнять
    этот атрибут, после нажатия на кнопку ( Найти ) страница перезагрузится,
    но форма полностью очистится.
Помимо этого заполнили атрибут class в некоторых тегах, чтобы форма выглядела
немного красивее.
----------------
В views.py добавил джинерик
class ProductsForm(ListView):
----------------
В simpleapp/urls.py добавил путь
path('products_form/', ProductsForm.as_view()),
---------------------------------------
===============================================================================
D_4                                                                     D_4
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

POST - запросы                                                   POST - запросы

!!!!!!!!!!!!!!!!!!!!!!!
Для передачи данных  POST - запросах используется тело запроса.
В самом URL вы его не увеличите. Его можно посмотреть с помощью Chrome DevToos
.

Рассмотрим как мог выглядеть запрос на -СОЗДАНИЕ ТОВАРА-

POST/products/create HTTP/1.1
Host: 127.0.0.1
Content-Type:application/x-www-form-urlencoded
Content-Length: 16
name=PythonBook&price=1000

Сначала указываем метод запроса (POST), путь (/products/create) и протокол (HTTP/1.1)
Host - адрес сервера на который отсылается запрос.
Content-Type - тип данных в теле запроса.
Content-Length - длина тела запроса.
Далее идёт само тело запроса.В нашем случае данные закодированы таким же образом,
как в параметрах GET- запроса.
GET - запросы используются, как правило, для того, чтобы получить какую-то
информацию с сервера, в то время как POST- запросы нужны для загрузки информации
на сервер. Хотя HTML- формы, должны быть написаны в HTML- файлах, Django
предоставляет нам инструменты генерации форм. В предыдущем юните мы пробовали
использовать формы. Тогда форму сгенерировал пакет django-filter.
Теперь создадим свою форму для модели товаров.
----------------
Создадим файл simpleapp/forms.py

from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

Создали собственный класс формы, наследуя ModelForm. Данный стандартный класс
позволяет создавать формы на основе моделей.
Саму модель прописываем в Meta классе в поле model=Product.
fields = '__all__' - означает что нужно из модели взять все поля,
кроме первичного ключа (его мы не должны редактировать).
В место этого мы могли и сами перечислить всеполя в ручную.
fields = [
    'name',
    'description',
    'quentity',
    'category',
    'price'
    ]
СОВЕТ:
       Для рабочих проектов лучше перечислять поля самостоятельно, чтобы не
       было ситуации, что добавили новое поле в модель, которое нельзя
       редактировать пользователям.
Как мы расположили поля в списке, в таком порядке они и будут выведены на
странице.
Это значит что мы сможем удобнее и логичнее вывести данные для заполнения.
----------------
Перейдём в shell                                              Перейдём в shell

pyton manage.py shell

>>> from simpleapp.forms import ProductForm

>>> f = ProductForm({'name': 'test', 'category': '1', 'price': 42, 'description': '', 'quantit
y': 1})
>>> f.is_valid()
False
Djano говорит нам что форма не валидна ( тоесть есть ошибка в заполнении )
>>> f.errors
{'description': ['This field is required.']} # не добавили описание

>>> f = ProductForm({'name': 'test', 'category': '1', 'price': 42, 'description': 'terof', 'qu
antity': 1})
>>> f.is_valid()
True

Для доступа к обработанным данным существует поле cleaned_data
>>> f.cleaned_data
{'name': 'test', 'description': 'terof', 'quantity': 1, 'category': <Category: Колбаса>, 'pric
e': 42.0}
Мы видим, что вместо id категории подставился объект модели,
а ена теперь имеет тип float
Если нам передадут в форму лишние данные, то при обработке они будут пропущены
и не возникнет никаких ошибок.
Добавим в форму лишний ключ 'extra_field'

f = ProductForm({'name': 'test', 'category': '1', 'price': 42,
'description': 'terof', 'quantity': 1, 'extra_field': 123})

>>> f.is_valid()
True
>>> f.cleaned_data
{'name': 'test', 'description': 'terof', 'quantity': 1, 'category': <Category: Колбаса>, 'pric
e': 42.0}

Если мы напечатаем объект формы, то увидим сгенерированный HTML.
Именно этот HTML- код будет добавдяться в шаблон, когда мы будем использовать
в нём формы.

>>> print(f)
<tr>
    <th><label for="id_name">Name:</label></th>
    <td>
      <input type="text" name="name" value="test" maxlength="50" required id="id_name">
   </td>
  </tr>
  <tr>
    <th><label for="id_description">Description:</label></th>
    <td>
      <textarea name="description" cols="40" rows="10" required id="id_description">
terof</textarea>
    </td>
  </tr>
  <tr>
    <th><label for="id_quantity">Quantity:</label></th>
    <td>
      <input type="number" name="quantity" value="1" required id="id_quantity">
    </td>
  </tr>
  <tr>
    <th><label for="id_category">Category:</label></th>
    <td>
      <select name="category" required id="id_category">
  <option value="">---------</option>
  <option value="1" selected>Колбаса</option>
  <option value="2">Велосипеды</option>
</select>
    </td>
  </tr>
  <tr>
    <th><label for="id_price">Price:</label></th>
    <td>
      <input type="number" name="price" value="42" step="any" required id="id_price">
    </td>
  </tr>
В полях HTML - формы уже проставлены значения из нашей: input c name="name"
имеет value="test", select name="category" в теге с option value="1" имеет
selected и так далее.

Помимо того, что форма может быть авто-сгенерирована на основе какой-либо модели,
Django позволяет создавать их, просто указывая поля. Этот метод похож на то как
мы описывали модели.
Для этого используется тело класса формы, а не вложенный в него Мета-класс.
Вот так выглядело бы создание формы при написании его без Мета-класса.
class ProductForm(forms.Form):
    name = forms.CharField(label='Name')
    description = forms.CharField(label='Description')
    quentity = forms.IntegerField(label='Quentity')
    category = forms.ModelChoiceField(label='Category',
    queryset='Category.objects.all(),)
    price = forms.FloatField(label='Price')

В ближайее время нам не понадобится эта возможность Django.
Подробнее здесь: https://docs.djangoproject.com/en/4.0/ref/forms/fields/
---------------------------------------
Бывают ситуации, когда мы не хотим записывать в БД всё, что присылают нам
пользователи. Например в прошлом юните мы создали цензурный фильтр который убирал
нецензурные слова. В реальной задаче мы могли бы вообще запретить сохранять
не нужные статьи (новости). В таком случае нам поможет проверка данных, которые
пользователь присылает нам в форму.
-------------------
Добавим ограничения - описание товара должно быть не менее 20 имволов и не должно
совпадать с названием товара.
Читать  документации здесь:
https://docs.djangoproject.com/en/4.0/ref/forms/api/#django.forms.Form.clean
В разделе про формы есть пункт, в котором указано, что, если мы хотим сделать
свои собственные проверки, нам нужно переопределить метод clean в форме.
Добавим проверкудлины поля description/

simpleapp/forms.py

from django import forms
from django.core.exceptions import ValidationError
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'category',
            'price',
            'quantity',
        ]

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("description")
        if description is not None and len(description) < 20:
            raise ValidationError({
                "description": "Описание не может быть меньше 20 символов."
            })
        return cleaned_data
----------------
Переопределили метод clean и реализовали в нём проверку.
Вызываем в методе clean из родительского класса и
сохоаняем данные формы в clean_data.
Получаем description и проверяем его значение. Если значение не проходит по
длине, то вызываем ошибку. В ошибке указываем название поля формы и текст оибки.
Если проверка прошла успешно, возвращаем из функции проверенные данные формы.
----------------
Идём в Shell

from simpleapp.forms import ProductForm

>>> f = ProductForm({'name': 'test', 'category': 1, 'price': 42, 'description': 'test', 'quant
ity': 1})
>>> f.errors
{'description': ['Описание не может быть меньше 20 символов.']}

Проверка работает.
-------------------
Проверка данных в двух полях:
simpleapp/forms.py

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("description")
        if description is not None and len(description) < 20:
            raise ValidationError({
                "description": "Описание не может быть меньше 20 символов."
            })

        name = cleaned_data.get("name")
        if name == description:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data
Добавили поле name для проверки.
--------------
Идём в Shell

>>> from simpleapp.forms import ProductForm
>>> f = ProductForm({'name': '12345678901234567890', 'category': '1', 'price': 42, 'descriptio
n': '12345678901234567890', 'quantity': 1})
>>> f.errors
{'__all__': ['Описание не должно быть идентично названию.']}

Так как мы не указали поле при создании ошибки, Django добавил ключ __all__,
который сообщает, что ошибка относится ко всей форме, а не к определённому полю.
---------------------------------------
Другой механизм валидации данных

from django import forms
from django.core.exceptions import ValidationError
from .models import Product


class ProductForm(forms.ModelForm):
    description = forms.CharField(min_length=20) # указали минимальную длину

    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'category',
            'price',
            'quantity',
        ]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        description = cleaned_data.get("description")

        if name == description:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data

Убрали проверку на длину описания из метода, добавили поле в саму форму и в этом
поле уже поставили ограничение на минимальную длину строки.
---------------
Для проверки работы идём в Shell

>>> from simpleapp.forms import ProductForm
>>> f = ProductForm({'name': 'test', 'category': 1, 'price': 42, 'description': 'test', 'quant
ity': 1})
>>> f.errors
{'description': ['Ensure this value has at least 20 characters (it has 4).']}

>>> f = ProductForm({'name': 'test', 'category': 1, 'price': 42, 'description': '1234567890123
4567890', 'quantity': 1})
>>> f.errors
{}
------------------
Всё хорошо. Валидация работает. Однако мы не сможем внести на уровень полей формы
совместную проверку текста в названии и описании.По этому для каждой задачи нужно
использовать свой инструмент.
------------------
Третий способ проверки валидации данных.
Позволяет проверить с помощью функции данные одного конкретного поля.
Ранее с помощью функции мы получали доступ к проверке всех полей вместе.
Например так можно проверить, написано ли название товара с заглавной буквы.

simpleapp/forms.py

def clean_name(self):
      name = self.cleaned_data["name"]
      if name[0].islower():
          raise ValidationError(
              "Название должно начинаться с заглавной буквы."
          )
      return name
-----------------
Выбирайте соответствующий способ валидации данных, исходя из задачи.
Если можно обойтись переопредилением формы
description = forms.CharField(min_length=20), то лучше воспользоваться им.
Если требуется проверить одно поле сложным образом, создайте для этого метод
clean_fieldname.
В случае необходимости использования нескольких полей одновременно
воспользуйтесь методом clean.
Комбинирование вариантов также допустимо.
---------------------------------------
Добавление страницы создания товара:

templates/product_edit.html

{% extends 'flatpages/default.html' %}

{% block content %}
<h1>Товар</h1>
<hr>
<form action="" method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Save" />
</form>
{% endblock content %}
---------------
В HTML - форме указывали method="get", а для передачи информации, которая
изменяет состояие БД (создаёт, изменяет, удаляет данные), будем указывать
method="post".
В шаблон добавим тег {% csrf_token }, он нужен для безопасной отправки данных
и защиты от хакерских атак.
Подробнее здесь: https://ru.wikipedia.org/wiki/Межсайтовая_подделка_запроса
и здесь: https://docs.djangoproject.com/en/4.2/ref/csrf/
----------------
Теперь чтобы форма заработала нужно:
Создать представление- связать нашу форму и шаблон
Зарегистрировать представление в urlpatterns - Django должен знать,
    какое представление и по какому пути будет выполняться.

Добавим новое представление в views.py
simpleapp/views.py

from django.views.generic import ListView, DetailView, CreateView
from .models import Product
# -----------------
from django.http import HttpResponse
from .filters import ProductFilter
from django.urls import reverse_lazy
from .forms import ProductForm
..........
....
# Добавляем новое представление для создания товаров.
class ProductCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = ProductForm
    # модель товаров
    model = Product
    # и новый шаблон, в котором используется форма
    template_name = 'product_edit.html'
----------------
Зарегисрируем новое представление в urelpatterns.

simpleapp/urls.py

from django.urls import path
from .views import (ProductsList, ProductDetail, ProductsForm, ProductCreate)


urlpatterns = [
            # path - означает ПУТЬ
            # В данном случае путь ко всем товарам останется пустым
            # Т.к. объявленное представление является классом, а Django ожидает
            # функцию, надо представить этот класс в виде view.
            # Для этого вызываем метод as_view.
    path('', ProductsList.as_view(), name='product_list'),
            # pk - это первичный ключ товара, который будет выводиться у нас в шаблон
            # int - указывает на то, что принимаются только целочисленные значения

    path('<int:pk>', ProductDetail.as_view(), name='product_detail'),
    path('products_form/', ProductsForm.as_view()),
    path('create/', ProductCreate.as_view(), name='product_create'),
]
-----------------
Всё работает но есть нюанс.
Мы увидим форму но после её отправки, получим ошибку
"ImproperlyConfigured at /products/create/
No URL to redirect to.  Either provide a url or define a get_absolute_url method on the Model."

Проблема в том, что Django не знает, какую страницу нужно открыть после создания
товара. И как видно по описанию, можем убрать проблему, добавив метод
get_absolute_url в модель.

Добавим:
simpleapp/models.py

class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    # Поле которое будет ссылаться на модель категории
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE,
                                 related_name='products')
    # все продукты в категории будут доступны через поле products
    price = models.FloatField(validators=[MinValueValidator(0.0)])

    def __str__(self):
        return f'{self.name.title()}: {self.description[:20]}'

    # Добавим absolute_urls

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])
-----------------------
Используем спец- функцию reverse, которая позволяет указывать не путь
вида /products/..., а название пути. Если вернуться к описанию путей в urls.py,
то увидим что мы добавили значения для аргументов name. Такой механизм обращения
удобен тем, что если мы захотим изменить пути, прийдётся вносить меньше
изменений в код, а значит, меньше вероятность пропустить какое-то место и
получить баг.

simpleapp/urls.py

rom django.urls import path
from .views import (ProductsList, ProductDetail, ProductsForm, ProductCreate)
urlpatterns = [
    # path - означает ПУТЬ
    # В данном случае путь ко всем товарам останется пустым
    # Т.к. объявленное представление является классом, а Django ожидает
    # функцию, надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('', ProductsList.as_view(), name='product_list'),
    # pk - это первичный ключ товара, который будет выводиться у нас в шаблон
    # int - указывает на то, что принимаются только целочисленные значения
    path('<int:pk>', ProductDetail.as_view(), name='product_detail'),
    path('products_form/', ProductsForm.as_view()),
    path('create/', ProductCreate.as_view(), name='product_create'),
]
Здесь выводится название в таком же виде, как описано в методе __str__
в моделе Product.
GET и POST - запросы работают по-разному. Главное отличие заключается в способе
передачи данных.
Для передачи информации в GET-запросах используется query string,
а в POST- тело запроса.
---------------------------------------
Добавим страницу изменения информации о товаре. Мы можем использовать одну и
ту же форму и для создания, и для обнавления товара. И не только форму--
будем использовать тот же шаблон, хотя никто не запрещает зделать разные формы
и шаблоны. Единственное, что будет отличаться - дженерик,
который будем наследовать в представлении.

simpleapp/views.py
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView
)

# Добавляем представление для изменения товара.
class ProductUpdate(UpdateView):
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'
------------------
И регистрируем представление в
simpleapp/urls.py

from .views import (
    ProductsList, ProductDetail, ProductsForm, ProductCreate, ProductUpdate
)
path('<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),
--------------
http://127.0.0.1:8000/products/3/update/
---------------------------------------
Удаление товара:
Для подтверждения удаления сделаем отдельный шаблон.

templates/product_delete.html

{% extends 'flatpages/default.html' %}

{% block content %}
<h1>Удаление товара</h1>
    <hr>
    <form action="" method="post">
    {% csrf_token %}
    <p>Удаляем "{{ object.name }}"?</p>
    <input type="submit" value="Delete"/>
    </form>
{% endblock content %}
----------------
В views.py добавим представление, которое реализует удаление товара.
simpleapp/views.py

from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)
from .models import Product
# -----------------
from django.http import HttpResponse
from .filters import ProductFilter
from django.urls import reverse_lazy
from .forms import ProductForm

# Представление удаляющее товар.
class ProductDelete(DeleteView):
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')
----------------------
В представлении мы также не указывали фоорму.
В место неё появляется поле success_url, в которое мы должны указать, куда
перенаправить пользователя после успешного удаления товара.
Логика работы reverse_lazy точно такая же, как и у функции reverse,
которую использовали в моделе Product.
-----------------------
Регестрируем новый путь в urls.py с ProductDelete в качестве обработчика.
simpleapp/urls.py

from .views import (
    ProductsList, ProductDetail, ProductsForm, ProductCreate,
    ProductUpdate, ProductDelete,
)
 path('<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
---------------------------------------
Дженерики требуют указание формы в классе:
CreateView - нужно сообщить Django, как сохранять передаваемые данные.
UpdateView - нужно собщать Django, как сохранять передаваемые изменения
в объекте БД.
-------------
Какие существуют подходы для валидации данных в формах?
clean - Можем переопределить метод и написать свои сложные проверки.
Описание полей формы с указанием ограничений в полях формы.
---------------------------------------
Для вывода поля фильтрации по датам понадобиться указать спец-тип в HTML
https://developer.mozilla.org/ru/docs/Web/HTML/Element/input/datetime-local
-----
Необходимо изучить информацию по следующим ссылкам и
постараться реализовать выбор даты.
Посмотрите как указан фильтр name:
https://django-filter.readthedocs.io/en/stable/guide/usage.html#the-filter

Вам потребуется дополнительно указать правельный тип поля формы в атрибуте widget.
Пример тут:
https://django-filter.readthedocs.io/en/stable/ref/widgets.html
===============================================================================

D_5                                                                       D_5

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
---------------------------------------
ИДЕНТИФИКАЦИЯ                                                  ИДЕНТИФИКАЦИЯ
---------------------------------------
Предоставление каких либо данных, которые могут сопоставить с БД
идентификаторов пользователей.
В качестве идентификаторов могут выступать:
• логин - строка, как правило, состоящая из латинских символов
• адрес лектрон-почты
• номер телефона
• числовой идентификатор (USER ID, оторый иногда обозначают как UID)
• номер банковской кары
• персональные данные другого рода ( номер СНИЛС )
Идентификация пользователя призвана спросить у пользователя: "Кто ты?"
Как только пользователь, используя различные виды идентификаторов, ответил
на этот вопрос, ситема проверяет наличие такого идентификатора в БД и,
в случа успеха, начинается следующий этап - аутентификация.
Соврименные информационные системы часто предоставляют несколько способов
идентификации. Например ГосУслуги ( по номеру телефона, электронной почты
 или СНИЛС )
---------------------------------------
Аутентификация                                                 Аутентификация
---------------------------------------
После того как сервис удостоверился, что пользователь с таким идентификатором
существует, он должен проверить действительно ли вы тот пользователь.
Различают четыре фактора аутенификации:
1. Нечто. ИЗВЕСТНОЕ пользователю. ( pin- код, одноразовые и многоразовые пароли,
    секретные слова, графические ключи, криптографические ключи)
2. Нечто. ИМЕЮЩЕЕСЯ у пользователя. Различные устройства, позволяющие
    подтвердить подлинность данных входа. ( смарт-карты,usb-токены)
3. Нечто. ПРЕСУЩЕЕ пользователю. К этой категории данных относят различного вида
    биометрику. (отпечатки пальцев, сканеры лица, сканеры сетчатки глаза,
    голос и рукописная подпись)
4. Нечто. АСОЦИИРОВАННОЕ с пользователем. Например, GPS-координаты устройства,с
    которого осуществляется вход. Естественно, что этот фактор аутентификации
    не может быть самостоятельным. Однако он может служить дополнительной
    проверкой на этапе аутенфикации.

Часто бывает, что этапы идентификации и аутентификации происходят паралельно-
 как минимум для пользователя. Однако это происходит не всегда, иногда
 сервис просит сначала ввести логин и только потом пароль.
---------------------------------------
Немного о паролях
1. Одноразовые ( пароли из СМС ) которые нужно ввести в опредилённый промежуток
    времени.
2. Многоразовые. Например: для входа достаточно ввести номер телефона, к которому
привязан аккаунт, а также одноразовый пароль, который приходит из официального
    бота (в случае если аккаунт уже авторизован на каком-то устройстве).
---------------------------------------
Многофакторная аутентификация                   Многофакторная аутентификация
---------------------------------------
Часто требуется использование нескольких видов аутентификаций.
1. Пользователь вводит известную ему пару: почта-пароль.
2. Система перенаправляет на страницу ожидания и отображает текст: "Уведомление
    отправлено на устройство__. Чтобы подтвердить свою личность, нажмите ДА в
    уведомлении".
3. Паралельно на телефон, на котором данный аккаунт уже авторизован, приходит
    уведомление о том, что некий пользователь пытается войти в аккаунт с другого
    устойства. В этом уведомлении указывается, с какого устройства и откуда
    пытаются войти в аккаунт. А также есть две кнопки "разрешить войти" и
    "запретить".
4. Если на телефоне было выранно "разрешить войти", пользователь получает
    доступ к сервисам с другого устройства - процес аутентификации завершается.
---------------------------------------
САРТСНА                                                               САРТСНА
---------------------------------------
Отдельно стоит сказать про ещё один фактор безопасности- капча (англ. CAPTCHA)
Полность автоматизированный публичный тест Тьюринга для различия компьютеров
 и людей. (картинка с сфетофорами)
---------------------------------------
Авторизация                                                         Авторизация
---------------------------------------
После успешной аутентификации пользователь может работать с сайтом ли преложением.
В зависимости от уравня прав, который сервис предоставляет пользователю с данным
идентификатором, пользователь получает доступ к отдельным частям веб-приложения.

Авторизация производит контроль доступа к различным ресурсам системы в процессе
работы пользователей. Получается, авторизация без пройденной заранее аутентификации
не имеет смысла.
Возможно вы встречались с ситуацией, когда при попытке попасть на какую-то
страницу,сайт вас уведомляет, что данная страница доступна только для авторизованных
пользователей (ошибка 401) или у вас не достаточно прав для просмотра данной
страницы (ошибка 403).

401 код ошибки говорит о том, что предоставленные данные аутентификации по
    какой-либо причине были отклонены сервером или донные аутентификации вообще
    небыли переданы серверу.
403 код ошибки говорит о том,что у пользователя нет доступа к запрашиваемому
    ресурсу. Тоесть сервер как бы говорит: "Я знаю кто вы. о у вас нет прав для
    доступа к данному ресурсу. Возможно вам нужно обратиться к админу ресурса
    за получением разрешений". Повторно клиент не должен посылать запросы на
    этот ресурс. Для другог пользователя этот ресурс может быть доступен.
---------------------------------------
OAuth                                                                   OAuth
---------------------------------------
1. Менеджеры паролей. Например: 1Password или Bitwarden. Но при их использовании
    возникает вопрос доверия разработчикам этих продуктов.
2. Аутентификация и авторизация на сервисе-клиенте с помощью сервиса-провайдера.
    Вам предлагается или заполнить форму регистрации, или зарегистрироваться
    припомощи других сервисов. Именно этот механизм называется OAuth.
Он предлагает более широкие возможности - например, если авторизовать (предоставить
опредилённые права) сервис-клиен на сервесе-провайдере, то новый сайт сможет
выполнять на основном аккаунте разрешённые действия без участия пользователя.
Например: Какие именно действия сможет выполнять сайт, скажет сам провайдер OAuth.
    "что сайт получит доступ к почте, информации о профиле и к управлению
    контактами"

Если мы регистрируемся с помощью сервиса1 в сервисе2, то сервис2 получит доступ
к опредилённым действиям в сервисе1 (публиковать статьи, просматривать список
друзей, редактировать документы).

Существует несколько протоколов, призванных выполнить схожие задачи - OpenID,
а также OAuth 1.0 и OAuth 2.0.

OpenID - призван только для аутентификации пользователя на стороне-клиенте с
    помощью аккаунта-провайдера.
Протоколы OAuth 1.0 и OAuth 2.0 - также позволяют осуществить авторизацию клиента
    на стороне провайдера - выполнять действия на аккаунте-провайдере с
    помощью клиентского веб-приложения.
---------------------------------------
Cookie                                                                Cookie
---------------------------------------
Браузер(клиент) и сервер общаются друг с другом посредством протокола HTTP
и его методов - GET, POST и других. Этот протокол является stateless - каждый
запрос действует независимо от других. Тем самым текущее состояние клиента
с точки зрения протокола HTTP никак не хранится на сервере.
Пример:
Доустим вы вошли на сайт. Пусть это будет интернет магазин, на котором вы
закинули в корзину товары, а оплату решили отлложить(вдруг ещё что-то захочется
купить). Закрыв сайт, вы прервали общение браузера и сервера. При следующей
попытке входа на сайт, вообще говоря, браузер и сервер вновь должны "познакомиться"
И корзина должна быть пустой. Однако на современных сайта вы обнаружите, что
корзина уже не пустая.
Одно дело, если бы вы авторизовались, и позиции в корзине асоциировались с вашим
аккаунтом, но совсем другое дело, когда вы не даёте серверу ничего.
Или всё-таки отдаёте?
------------------
В силу отсутствия встроенного хранения состояния в протоколе HTTP, релизовали
хранение инормации cookie (куки, англ.-печенье)

Cookie - это информация, которую хранит браузер по просьбе сервера веб-приложения.

В таком случае, браузер при отправке зпроса на сервер, может вновь отправить
cookie с какой-то пользовательской информацией. Хранить конфиденциальную информацию
в cookie небезопасно. Проблема в том, что эта информация передаётся в виде
чистого текста, и сама по себе не является защищённой. Поэтому cookie чаще всего
используют для хранения идентификаторов, которые нельзя подобрать, или информации
которая не требует безопасного использования.
---------------------------------------
Сессии                                                                  Сессии
---------------------------------------
Это более безопасный механизм. Отличие сессии от чистого использования cookie
в том, что реальная информация хранится на сервере приложения, а в самих cookie
хранится только идентификатор сессии.
Идентификатор суссии и информация на сервере- это как номер заказа и сами
товары в заказа. С номером заказа (идентификатором сессии) вы приходите в магазин
(на сервер) и получаете товары (информацию от сервера).

Механизм сессии должен быть реализован разработчиком самостоятельно, т.е. он не
является встроенным механизмом, предоставляет протокол передачи данных (HTTP
или другие). Получается, что от разроботчика зависит на сколько безопасно и
качественно он реализует тот механизм.

Django - для работы с сессиями существует "решение из коробки". Этот модуль
аввтоматически подключается к каждому поректу.

settings.py
INSTALLED_APPS = [
    ... ,
    'django.contrib.sessions',
    ...
    ]
MIDDLEWARE = [
    ... ,
    'django.contrib.sessions.middleware.SessionMiddleware',
    ]
Данное приложение выполняет эту задачу - управление сессиями.
В обработке каждого запроса (переменная request) вы можете получить доступ к
данным сессии (которые храняться на сервере) и каким-то образом манипулировать ими.
Рассмотрим, как в общем виде происходит процес обмена данными между браузером
и сервером в случае наличия сессии.

Процесс прохождения запроса по мидлваре сессии и аутентификации с последующей
выдачей ответа из приложения:
1. При отправке запроса (request) на сервер, браузер с помощью cookie отправляет
    идентификатор сессии.
2. Сервер считывает этот идентификатор и смотрит в базе в таблице django-session
    его наличие.
3. Если сессия, согласно БД, является активной, пользователь автоматически
    проходит процедуру аутентификации, получая доступ к функциям приложения.
4. В зависимости от результата авторизации сервер обрабатывает запрос (внутри
    представления view), при необходимости сохраняя данные в сессии.
5. После чего формируется ответ сервера (response), в котором помимо прочего
    вновь отправляется идентификатор сессии, если это необходимо.
---------------------------------------
Дополнительный механизм безопасности работы с сессиями.

На некоторых сайтах, в настройках безопасности, можно найти список активных
сессий этого аккаунта. В этом списке можно увидеть устройство(браузер,десктопное
или мобильное приложение), дату последнего входа и другие данные.
При необходимости можно завершить одну или все сессии сразу. Это очень удобный
механизм защит, если вы например зашли в VK не со своего компьютера, но забыли
"выйти"(авершить сессию). Заходя через другое устройство, вы можетезакрыть
эту сессию.
---------------------------------------
Ограничение доступа к страницам                 Ограничение доступа к страницам
---------------------------------------
Как и в случае управления сессиями, в Django поддержка авторизации реализуется
в виде приложения, автоматически подключаемого к каждому новому проекту.
INSTALLED_APPS = [

    'django.contrib.auth',
    ]
Приложение django.contrib.auth предоставляет два решения для предоставления
доступа к представлениям только для зарегистрированных пользователей.
• декоратор login_required
• миксин LoginRequiredMixin
---------------------
Декоратор login_required

Содержится в пакете django.contrib.auth.decorators
Декоратор рекомендуется использовать для функций-представлений.

from django.contrib.auth.decorators import login_required

@login_required
def show_proteced_page(request):
    // do something protected

Представление в виде функции мы реализовывали в модуле D_4, юнит 3.
https://docs.djangoproject.com/en/4.0/topics/http/views/
---------------------------------------
Миксин LoginRequiredMixin
Использовать миксин LoginRequiredMixin также просто: его необходимо добавить
в список наследуемых класов при создании представления.
Добавил в класс!!!!!!!!!!!!!!!!!!!!!!!!!!!!
simpleapp/view.py
from django.contrib.auth.mixins import LoginRequiredMixin

class ProductCreate(LoginRequiredMixin, CreateView):
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'
----------------
А что произойдёт, когда страницу откроет не аутентифицированный пользователь?

Если представление использует миксин LoginRequiredMixin, все запросы не
аутентифицированных пользователей будут перенаправлены на страницу входа, или
будут показаны ошибки HTTP 403 Forbidden, в зависимости от параметра raise_exception.
 Параметр raise_exception мы не добавляли.
 И страница входа, которая например должна быть указана в settings.py в переменной
LOGIN_URL, тоже не указана в нашем проекте.
Если мы попробуем открыть страницу (product/create) то получим ошибку 404, а
в строке запроса у нас будет
http://127.0.0.1:8000/accounts/login/?next=/products/create/
Видим что страница "/accounts/login/" не найдена. Оказывается страница входа
имеет значение по умолчанию.
Подробнее здесь:
https://docs.djangoproject.com/en/4.0/ref/settings/
LOGOUT_REDIRECT_URL
PASSWORD_RESET_TIMEOUT
---------------------------------------
Ошибка 403                                                          Ошибка 403
---------------------------------------
Настроим выдачу ошибки с кодом 403, для не авторизованных пользователей, которые
будут заходить на страницу создания товара.

simpleapp/view.py

class ProductCreate(LoginRequiredMixin, CreateView):

    raise_exception = True  # Добавил обработку ошибки 403

    # Указываем нашу разработанную форму
    form_class = ProductForm
    # модель товаров
    model = Product
    # и новый шаблон, в котором используется форма
    template_name = 'product_edit.html'
-------------------
Django позволяет установить свою страницу для отображения 403 ошибки.
Создал:
template/403.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ошибка 403</title>
</head>
<body>
<h1>Кажется у вас нет доступа к этой странице</h1>
</body>
</html>
-------------------
Больше нигде регистрировать не нужно. При появлении 403 ошибки Django сам пойдёт
искать файл с таким названием у нас в папке с шаблонами. Раньше его небыло и он
выводил свою стандартную страницу.
При этом, если авторизоваться через страницу админа то страница создания тоара
откроется.
---------------------------------------
Вход                                                                    Вход
---------------------------------------
!!!!!!!!!

Сделаем свою страницу входа для пользователей.
Добавим urls приложения, с которым ранее работали в этом модуле -
"django.contrib.auth".
Django скажет, как обрабатывать запросы от пользователей по ссылкам, которые
начинаются с /accounts/.
Это основной urls/py
django_d4/urls.py

path('accounts/', include('django.contrib.auth.urls')),
-----------------
теперь нам стали доступны новые пути:
• accounts/login/ [name='login']
• accounts/logout/ [name='logout']
• accounts/password_change/ [name='password_change']
• accounts/password_change/done/ [name='password_change_done']
• accounts/password_reset/ [name='password_reset']
• accounts/password_reset/done/ [name='password_reset_done']
• accounts/reset/// [name='password_reset_confirm']accounts/reset/done/
[name='password_reset_complete']
---------------------
Подробнее здесь:
https://docs.djangoproject.com/en/4.0/topics/auth/default/
All authentication views¶
This is a list with all the views django.contrib.auth provides.
For implementation details see Using the views.

class LoginView¶
---------------------------------------
Пути и представления Django нам предоставил, а вот шаблоны мы должны описать сами.
Добавим шаблон. Форма для регистрации пользователя

templates/registration/login.html

{% extends 'flatpages/default.html' %}

{% block content %}
    <form method="post" action="{% url 'login' %}">
        {% csrf_token %}
        {{ form.as_p }}
        <input type="submit" value="login">
        <input type="hidden" name="next" value="{{ next }}">
    </form>
{% endblock content %}
----------------
Но после ввода логина и пароля нам высвечивается ошибка.
По умолчанию после входа Django пытается перенаправить нас на страницу профиля,
которой пока нет.
Настроим так, чтобы после входа нас перенаправляло на страницу списка товаров.
В настройках нужно указать путь в переменной LOGIN_REDIRECT_URL.
Подробнее здесь:
https://docs.djangoproject.com/en/4.2/ref/settings/
LOGIN_REDIRECT_URL¶
-------------
django_d4/settings.py

STATIC_URL = 'static/'

LOGIN_REDIRECT_URL = "/products"  # Добавил ссылку на страницу для
    перенаправления после входа пользователя
---------------------------------------
Добавил ссылки на изменение и удаление товара
products.html
 <tr>
    <td>{{ product.name }}</td>
    <td>{{ product.description|truncatewords:2 }}</td>
    <td>{{ product.category.name }}</td>
    <td>{{ product.price|currency:"rub" }}</td>
    <td>{{ product.quantity }}</td>
    <td><a href="{% url 'product_update' pk=product.id %}">Изменить</a></td>
    <td><a href="{% url 'product_delete' pk=product.id %}">Удалить</a>  </td>
</tr>
---------------------------------------
Регисрация                                                          Регисрация
---------------------------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Создаём отдельное приложение для регистрации пользователей
python manage.py startapp accounts
---------------------------------------
Создаём форму в:
accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )
---------------------------------------
Для облегчения этой задачи в модуле аутентификации есть базовая форма, позволяющая
создать пользователя(в ней реализованы все проверки и валидации). По умолчанию
она имеет только поле username и два поля для пароля.
Расширим эту форму добавив поля - электронная почта, имя и фамилия нового пользователя.
Эти поля есть в модели User.
---------------------------------------
Создадим представление
accounts/views.py

from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import SignUpForm

class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'

Клас имеет несколько атрибутов:
• модель формы, инстанс который будет создавать дженерик
• форма которая будет заполняться пользователем
• URL, на который нужно направить пользователя после успешной обработки формы
• шаблон, в котором будет отображенаформа
---------------------------------------
Добавим шаблон:
templates/registration/signup.html

{% extends "flatpages/default.html" %}

{% block content %}
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <input type="submit" value="Sing up">
    </form>
{% endblock content %}
---------------------------------------
Теперь подключим в urlpatterns, чтобы регистрация стала доступна на сайте.
Для этого создадим и заполним фаил urls.py в нашем новом приложении.
accounts/urls.py

from django.urls import path
from .views import SignUp

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
]
---------------------------------------
Подключим urls приложения account в главном приложении django_d4.
django_d4/urls.py

path('accounts/', include('django.contrib.auth.urls')),
path('accounts/', include('accounts.urls')), # Добавил путь
---------------------------------------
Префикс путей стандартного приложения auth и accounts совпадает. Ошибок это не
вызовет. Django будет искать подходящий путь для обработки по очереди, как
указано в списке - сначало в django.contrib.auth.urls, если не найдёт, то будет
искать в accounts.urls
Так как django.contrib.auth.urls не было пути signup, все запросы на
/accounts/signup будут успешно доходить до нашего представления SignUp
---------------------------------------
После регистрации нас перенаправит на страницу входа.
---------------------------------------
OAuth                                                                  OAuth
---------------------------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
OAuth - позволяет для регистрации на одном сайте использовать данные с другого
ресурса (зарегистрироваться с помощью аккаунта гугла).
------------
Установим - пакет allauth
pip install django-allauth
----------
Нужно его настроить
django_d4/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'simpleapp',
    'django_filters',
    'accounts',

    # Добавил 3 обязательных приложения allauth и одно, которое отвечает
    за вход через yndex

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',
    ]
---------------
SITE_ID = 1
---------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',

                    # allauth обязательно нужен этот процессор
                'django.template.context_processors.request',
                    ----------
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
-----------------
Этого раздела может не быть, нужно добавить

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
---------------------------------------
И так в первую очередь нужно удостовериться, что в конфигурации шаблонов присутствует
контекстный процессор  'django.template.context_processors.request',
----------
Долее нам необходимо добавить бэкенды аутентификации:

• встроенный бэкенд django - 'django.contrib.auth.backends.ModelBackend'-
    реализующий аутентификацию по username
• бэкенд аутентификации, предоставленный пакетом allauth
    'allauth.account.auth_backends.AuthenticationBackend',
---------
Грубо говоря, нам нужно включить аутентификацию как по username, так и специфичную
по emaill или сервис-провайдеру.
---------
В установленных приложениях необходимо убедиться в наличии
некоторых встроенных приложений Django, которые добавляют:
• пользователей - 'django.contrib.auth',
• сообщения - 'django.contrib.messages',
• настройки сайта - 'django.contrib.sites',
---------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

    # добавил строку без неё миграции не проходят

    'allauth.account.middleware.AccountMiddleware',
]
---------
Также нужно подключить приложения из пакета allauth (три обязательных приложения
    для работы allauth и одно, которое добавит поддержку входа с помощью Yandex).

settings.py

INSTALLED_APPS = [
    ......
    'simpleapp',
    'django_filters',
    'accounts',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',
    ]
---------
SITE_ID - используется в случае, если данный проект управляет несколькими сайтами.
    Сейчас для нас это не важно. Достаточно прописать значение 1 для этой переменной.
---------
После модификации файла настроек обязательно нужно выполнить миграцию.
Иначе необходимые модели из подключенных приложений не создадутся в нашей БД.
---------------------------------------
Регистрация по emaill и паролю                  Регистрация по emaill и паролю
---------------------------------------
!!!!!!!!!!!!!
В файл настроек проекта внесём дополнительные параметры, в которых укажем обязательные
и необязательные поля.
Обязательность остаётся на усмотрение разработчика.
В нашем случае укажем следующюю комбинацию параметров
django_d4/settings.py

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'

-------
Первые два параметра указывают на то что поле email является
обязательным и уникальным.
Третий говорит что поле username необязательный.
Следующий что атентификация будет происходить посредством электронной почты.
Напоследок указываем, что вертификация почты отсутсутствует. Обычно на почту
отправляется подтверждение аккаунта, после подтверждения коороговостанавливается
полная функциональность учётной записи. Для тестового примера нам необязательно
это делать.
---------
После этих настроек, нужно заглянуть в главный файл URL и внести изменения,
чтобы по accounts было доступно только приложение allauth.
django_d4/urls.py

from django.contrib import admin
from django.urls import path, include
from simpleapp.views import multiply

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    # Делаем так, чтобы все адреса из нашего приложения (simpleapp/urls.py)
    # подключались к главному приложению с префиксом products/.
    path('products/', include('simpleapp.urls')),
    path('multiply/', multiply),
        # path('accounts/', include('django.contrib.auth.urls')),
        # path('accounts/', include('accounts.urls')),

    path('accounts/', include('allauth.urls')), # вот этот
]
----------
Теперь для регистрации необходимо ввести только email и пароль.
---------------------------------------
Регистрация и вход через Yandex                Регистрация и вход через Yandex
---------------------------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
В случае регистрации и входа через провайдера необходимо проделать ещё некоторые
действия, чтобы allauth знал, какие данные передавать Yandex при регистрации
пользователя, а Yandex знал, что наш сайт будет к нему обращаться.
---------
Добавим настройки сайта, которые требуются для allauth

1. Войдём в панель администратора
    • http://127.0.0.1:8000/admin/
    • вкладка Sites - отредактировать объект Site
        Domain name: 127.0.0.1
        Display name: example.com # и сохранить
2. Регистрируем приложение в Yndex для работы с сервисом
    • Преходим https://oauth.yandex.com/client/new и заполняем обязательные поля
        • General
            • Service name - SkillFactoryTest
        • Platforms
            • Choose at least one platform
                х Web setvices
                  Redirect URI
                  URL the user is redirected to after allowing or denying access to the app
                     http://127.0.0.1:8000
                     http://127.0.0.1:8000/accounts/yandex/login/callback
        • Data access
            To add a permission, enter its name
                Permission name # поле для выбора по каким полям проходит регисрация
                Access to email address # у нас заявлено что по emaill
                login:email
                - # и по username
                Access to username, first name and surname, gender
                login:info
----------- Это ТО что написанно в юните
    • App name: любое название например, SkillFactoryTest
    • URL to app site: http://127.0.0.1:8000
    • Callback URL: http://127.0.0.1:8000/accounts/yandex/login/callback
    • Permisions>Yandex.Passport API: выбрать пункты
        Adress to email address и
        Access to username, first name and surname, gender

        Видео: 17 D5 Курсс 11:15 время
3. Подтверждаем создание приложения и видим секретные данные. Они нам понадобятся
    для регистрации провайдера в нашем Django проекте.
4. Секретные данные теперь нужно перенести в наше преложение.
    Открываем админку: http://127.0.0.1:8000/admin/socialaccount/socialapp/add/

Home › Social Accounts › Social applications › Add social application

    Provider: Yandex
    Name: любое имя например Yandex
    Client id: ID с страницы приложения Yndex. Поле: "ClientID"
    Seret key: Password с страницы приложения Yandex. Поле: "Client secret"
    Sites переносим единственный сайт в Chosen sites
И сохраняем.
------------
Эти данные и их заполнение в панели администратора можно считать универсальным
шаблоном. При работе с другими провайдерами отличаться будет только сам процесс
регистрации приложения на стороннем сайте. Все поля в нашем приложении будут
заполняться так же.

Вот так мы говорим allauth, что существует провайдер Yandex и вот данные для
работы с этим провайдером. Введённую нами информацию allauth будет использовать
для регистрации пользователя с помощью стороннего сайта,  нашем случае это Yandex.
Сохраняем и переходим : http://127.0.0.1:8000/accounts/login/ нажимаем на
ссылку Yandex. Открывается страница подтверждения входа через Yandex.
Нажимаем Continue.
-------
Должно перекинуть на страницу входа в аккаунт Yndex или сразу на подтверждение
входа.
Yndex уточнит, точно ли мы хотим войти в приложение, используя данные аккаунта
с сайта Yndex.
После подтверждения система перенаправит пользователя на главную страницу со
списком товаров.
При этом в БД появится запись о новом пользователе.
А в cocial accounts появится запись о том, что новый пользователь
зарегистрировался через Yndex.
---------------------------------------
Группы пользователей                                     Группы пользователей
---------------------------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!
В Django - сначала создаём группу а потом добавляем в неё пользователей.
---------------------------------------
Работа с панелью администратора
------------
По умолчанию в Django управлять группами можно двумя способами:
• из панели администратора
• программно создавать, редактировать и удалять объекты модели Group
------------
Через панель администратора самый простой способ
Панель администратора - Groups - Add group
Название и сохраняем.
---------------------------------------
Пользователи группы, а точнее их модели имеют тип связи ManyToMany (многие-о-многим)
Один и тот же пользователь может принадлежать нескольким группам.
---------------------------------------
Создадим группы
    common users
	managers
---------
Добавим ползователей в группы
Для этого в админ-панеле откроем страницу с профилем юзера, в окошке доступных
групп выберем в какой или в каких группах он будет состоять
Permissions
Groups:
Available groups
список доступных групп

В профиль юзера можно зайти и так:
http://127.0.0.1:8000/admin/auth/user/1/change/
Это будет первый юзер
---------------------------------------
Добавление в группы при регистрации        Добавление в группы при регистрации
---------------------------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Существует несколько способов:
• Использовать систему сигналов - оторые могут передавать модели.
• Переопределить класс формы так, чтобы при успешном прохождении регистрации
    добавлять присоединение к базовой (common user) группе пользователей.
---------------------------------------
Для этого изменим форму SignupForm полностью переписав файл
accounts/forms.py

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        common_users = Group.objects.get(name="common users")
        user.groups.add(common_users)
        return user
------------
Здесь мы импортировали класс формы, который предоставляет allauth, а также
модель групп. В кастомизированном классе формы, в котором мы хотим добавить
пользователя в группу, нужно переопредилить только метод save(), который
выполняется при успешном заполнении формы регистрации.
    В первой строке метода мы вызываем этот же метод родителя, чтобы необходимые
проверки и сохранение в модели User были выполненны.
    Далее мы получаем объект модели группы с названием common users.
    И в следующей строке мы доюавляем нового пользователя в эту группу.
Обязательным требованием метода save() является возвращение объекта модели
User по итогу выполнения функции.
-------------
Чтобы allauth распознал нашу форму как ту,что должна выполняться вместо формы
по умолчанию, необходимо добавить строчку в фаил настроек проекта settings.py
django_d4/settings.py

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'
# добавили
ACCOUNT_FORMS = {"signup": "accounts.forms.CustomSignupForm"}
-------------
Путь до формы ("accounts.forms.CustomSignupForm") у нас состоит из указания
приложения accounts, файла forms и класса формы CustomSignupFor.
-------------
Посмотрим как всё работает, создадим пользователя:
http://127.0.0.1:8000/accounts/signup/
-------------
Заодя на страниц этого пользователя, видим что он находится в группе.
Всё работает.
---------------------------------------
Добавление группы будет радотать только для пользователей, которые регистрируются
с помощью почты и пароля. Для тех кто регистрируется через сторонние сервисы,
форма которую мы изменили не будет выполняться, и в группу добавляться он
небудет.
---------------------------------------
Для решения этой задачи можно использовать механизм сигналов.
В Django есть специальный механизм сигналов, при возникновении которых могут
вызываться указываемые разработчиком функции. В документации allauth (
https://django-allauth.readthedocs.io/en/latest/account/signals.html?
highlight=allauth.account.signals.user_signed_up#signals
есть список таких сигналов. Из них мы можем выбрать тот, который овечает за
регистрацию пользователя, (allauth.account.signals.user_signed_up) и указать,
что при его
возникновении должна выполняться функция добавления пользователя в группу.
В документации Django есть целый раздел посвященный сигналам.
https://docs.djangoproject.com/en/4.2/ref/signals/
---------------------------------------
Права доступа                                                     Права доступа
---------------------------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Для этого войдём в соотвецтвующую страницу пользователя или группы переместим
разрешения в правую колонку.
Группа managers

simpleapp |product|Can add product
simpleapp |product|Can change product
simpleapp |product|Can delete product
------------
Теперь группа менеджеров имеет права на создание, изменение и удаление товаров.
------------
А вот так добавление группе менеджеров прав на создание товаров
выглядит в виде Pthon кода:

managers = Group.objects.get(name='managers')
perm = Permission.objects.get(name='Can add product')
managers.permissionsadd(perm)
-------------
Однако назначение прав в админке не каак не изменит работу проекта.
Ведь мы нигде не указали, где эти права должны проверяться и применяться.
---------------------------------------
Проверка прав в представлении                   Проверка прав в представлении
---------------------------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Мы уже знакомились с миксином LoginRequiredMixin.
Проверкуправ добавить будет не сложнее.
В классе-представлении мы должны добавить миксин PermissionRequiredMixin,
чтобы Django проверял у пользователя, который будет делать запрос, наличие
указанных нами прав.
Пример:

from django.contrib.auth.mixins import PermissionRequiredMixin

class MyView(PermissionRequiredMixin, View):
    permission_required = ('<app>.<action>_<model>',
                           '<app>.<action>_<model>')

По этому примеру добавим проверки в наши старые представления:

simpleapp/views.py

from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
class ProductCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_product',) # Добавил проверку прав
    # raise_exception = True
    # Указываем нашу разработанную форму
    form_class = ProductForm
    # модель товаров
    model = Product
    # и новый шаблон, в котором используется форма
    template_name = 'product_edit.html'

По этому примеру делаем с представлениями
class ProductUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('simpleapp.add_product',)

class ProductDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('simpleapp.add_product',)
---------------------------------------
Проверка прав в шаблоне                                 Проверка прав в шаблоне
---------------------------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Теперь получаетя так, что ссылки на заблокированные страницы выводятся всемпользователям
А заблоктроваными они будут для всех клиентов магазина, то есть для подавляющего
количества пользователей. Пользователи будут на них нажимать и получать ошибки.
Это не очень хорошо.
Чтобы скрыть лишние ссылки, можно установить проверки в самом шаблоне:

templates/products.html

    {# Теперь будем проверять не request.user.is_authenticated, а конкретные права #}

{% if perms.simpleapp.add_product %}
     <a href="{% url 'product_create' %}">Создать</a>
{% endif %}

                  <hr>
                        {% if products %}
                            <table>
                                 <tr>
                                    <td>Название</td>
                                    <td>Описание</td>
                                    <td>Категория</td>
                                    <td>Цена</td>
                                    <td>Количество</td>

{# Условие получается составным #}
{% if perms.simpleapp.change_product or perms.simpleapp.delete_product %}
    <td>Действие</td>
{% endif %}

                </tr>
                {% for product in products %}
                <tr>
                    <td>{{ product.name }}</td>
                    <td>{{ product.description|truncatewords:2 }}</td>
                    <td>{{ product.category.name }}</td>
                    <td>{{ product.price|currency:"rub" }}</td>
                    <td>{{ product.quantity }}</td>

<td>
   {# А здесь доступ к каждой ссылке будет проверяться отдельно #}
    {% if perms.simpleapp.change_product %}
        <a href="{% url 'product_update' pk=product.id %}">Изменить</a>
    {% endif %}
    {% if perms.simpleapp.delete_product %}
        <a href="{% url 'product_delete' pk=product.id %}">Удалить</a>
    {% endif %}
</td>
                </tr>
                {% endfor %}
            </table>
        {% else %}
            <h2>Товаров нет!</h2>
        {% endif %}
-------------
Теперь у нашего пользователя даже ссылки не видны.
-------------
Чтобы ссылки появились, можно в панели администратора раздать права как группе
пользователей так и отдельному пользователю.
---------------------------------------
Если обобщить, то можно сказать, что авторизация сводится к двум этапам:
• ограничению прав для тех или инных действий на сайте (например, через
    PermissionRequiredMixin);
• предоставлению прав для отдельных пользователей и/или групп.
---------------------------------------
D_6                                                                     D_6
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
---------------------------------------
Настройка и отправка писем                         Настройка и отправка писем
---------------------------------------

Для начала нужно настроить "отправителя" сообщений и указать данные нашей почты,
с которой будут отправляться письма.
    Отправителем в Django выступает один из спец. Python-классов. По анологии
с обычным использованием почты можно считать, что данный класс играет роль
почтовой программы. Так же как mail.yndex.ru, н умеет отправлять сообщения на
другие почтовые ящики. Но получить и прочитать входящие сообщения не получится.
Можем только отправлять письма.
    Для настройки класса используется переменная EMAIL_BACKEND в settings.py.
По умолчанию эта переменная содержит значение
"django.core.mail.backends.smtp.EmailBackend". Это класс, который использует
стандартную библиотеку Python для работы с SMTP - протоколом отправки
сообщений.
    Есть и другие классы для работы с почтой в Django, но они используются для
разработки и тестирования. например существует класс
"django.core.mail.backends.console.EmailBackend", который в место отправки
письма по электронной почте просто напечатает его в консоли.

Долее нужно настроить в проекте доступ к нашей почте, от чьего имени будут
отправляться письма.
-------------------
В зависимости от того , где увас зарегистриван почтовый адрес, настройки будут
слегка отличаться. Кроме логина и пароля, нас интерисуют параметры для работы с
 почтовым сервером по протоколц SMTP.

• адрес почтового сервера
• порт
• необходимость использования SSL (защищённого соединения).
-------------------
Вот парпметры для настройки почтового ящика от Yandex и GMail.
Плюс для Yandex нужно разрешить работу с помощью парлей приложений.

Почта-→Все настройки-→Почтовые пограммы
Разрешить доступ к почтовому ящику с помощью почтовых клиентов
 ◙ С сервера imap.yandex.ru по IMAP
    Способ авторизации по IMAP
     ◙ Пароли приложений и OAuth-токены
○ Отключить авто удаление писем, помеченных в IMAP как удалённые
○ С сервера pop.yandex.ru по протоколу POP 3
-------------------
Настроить данные по работе с почтовым сервером:

• EMAIL_BACKEND - класс отправителя сообщений (у нас установленно это значение
    по умолчанию а значит, эта строчка не обязательна)
• EMAIL_HOST - хост почтового сервера
• EMAIL_PORT - порт, на который почтовый сервер принемает письма
• EMAIL_HOST_USER - логин пользователя почтового сервера
• EMAIL_HOST_PASSWORD - пароль пользователя почтового сервера
• EMAIL_USE_TLS - необходимость использования TLS (зависит от почтового сервера
                смотрите документацию по настройке работы сервера по SMTP)
• EMAIL_USE_SSL - необходимость использования SSL (зависит от почтового сервера
                смотрите документацию по настройке работы с сервером по SMTP)
• DEFAULT_FROM_EMAIL - почтовый адрес отправителя по умолчанию
--------------------
Вот так может выглядеть блок кода настроек нашего проекта работы с
Yandex-почтой
Добавим в:
django_d4/settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = "si-mart" # Без @yandex.ru
EMAIL_HOST_PASSWORD = email_host_password  # config.py
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = "si-mart@yandex.ru"

DEFAULT_FROM_EMAIL = "example@yndex.ru" # эта строчка будет использоваться как
                        значение по умолчанию для поля from в письме.будет
                        отображаться в поле "отправитель" у получателя письма.
-------------------
Отправка письма                                             Отправка письма
-------------------
Теперь нужно понять где и какой код писать для отправки письма новому
пользователю. Изменим форму регистрации новых пользователей.
Полностью переписав форму регистрации.

accounts/forms.py

from allauth.account.forms import SignupForm
from django.core.mail import send_mail

class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)

        send_mail(
            subject='Добро пожаловать в наш интернет-магазин!',
            message=f'{user.username}, вы успешно зарегистрировались!',
            from_email=None, # Будет использованно значение DEFAULT_FROM_EMAIL
            recipient_list=[user.email],
        )
        return user
-------------------
Функция send_mail позволяет отправить письмо указанному получателю в
recipient_list. В поле subject мы передаём тему письма, а в message - текстовое
 сообщение.
---------------------------------------
Письма с HTML                                                   Письма с HTML
---------------------------------------
!!!!!!!!!!!!!!!!!!!!!!!
Кроме обычных текстовых писем мы можем отправлять пользователю текст с HTML.
Это позволит нам выделить слова с помощью жирного начертания (тег <b>) и
применять другие HTML теги.
    Чтобы отправить HTML по почте, лучше всего воспользоваться спец-классом
EmailMultiAlternatives. Он позволяет отправить текстовое сообщение и приложить
к нему версию с HTML разметкой. Таким образом почтовые клиенты которые могут
отображать HTML, покажут его, а те у кого нет такой функциональности, выведут
пользователю текстовую версию.
-------------------
Обновим код нашей формы, добавив отправку HTML-версии письма.
accounts/forms.py

from allauth.account.forms import SignupForm
from django.core.mail import EmailMultiAlternatives

class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        subject = 'Добро пожаловать в наш интернет-магазин!'
        text = f'{user.username}, вы успешно зарегистрировались!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'<a href="http://127.0.0.1:8000/products">сайте</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()
        return user
-------------------
Тема письма (subject), отправитель (from_email) и получатель(to) укзывается
точно так же, как и в предыдкщем примере.
    А вот переменные (text и html) содержат две переменные одного письма:
текстовую и HTML.
В инициализатор класса EmailMultiAlternatives мы передаём текстовую версию а
html прикрепляем как альтернативный вариант письма.
После чего отправляем составленное письмо.
-------------------
Если вы будете писать данные сообщения с большим количеством разметки, то
советуем внести код в HTML-файл и с помощью функции render_to_string создать
переменную с HTML-кодом. И уже эту переменную передать в attach_alternative.
    То есть, по сути, разработать шаблон не для выдачи в браузере, а для
составленя письма.
---------------------------------------
Рассылка менеджерам и администраторам     Рассылка менеджерам и администраторам
---------------------------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Django предоставляет спец-функцию для отправки сообщения набору администраторов
и менеджеров. Для этого в настройках проекта нужно создать и описать группу
администраторов и менеджеров, после чего вызвать функцию mail_admins или
mail_managers. Они отвечают за отправку писем.
    Например: нам требуется сообщить о новых пользователях всем менеджерам
сайта.
    Добавим переменную SERVER_EMAIL, где будет содержаться адрес почты, от
имени которой будет отправляться письмо при вызове mail_admins и
mail_manager. А переменная MANAGERS будет хранить список имён менеджеров и
адресов их почтовых ящиков.

django_d4/settings.py

SERVER_EMAIL = "si-mart@yandex.ru"
MANAGERS = (
    ('Ivan', 'feronts@mail.ru'),
    ('Petr', 'matveykey@mail.ru'),
    ('Bob', 'den_vo@mail.ru'),
)
-------------------
После чего в форме отправим им сообщение с помощью функции mail_managers:

accounts/forms.py

from allauth.account.forms import SignupForm
from django.core.mail import mail_managers


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)

        mail_managers(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )
        return user
-------------------
В начале темы письма добавилась надпись [Django]. Эту надпись фреймпорк
добавляет автоматически.
    Её можно изменить с помощью переменной
EMAIL_SUBJECT_PREFIX в настройках проекта. По умолчанию она [Django].
-------------------
Рассылка администраторам делается точно также, только используется переменная
ADMINS в настройках приложения и функция mail_admins при отправке сообщения.
---------------------------------------
Подтверждение mail по почте                        Подтверждение mail по почте
---------------------------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Теперь мы готовы настроить allauth для пдотверждения адресов пользователей,
чтобы в дальнейшем посылать письма на корректные почтовые ящики.
-------------------
К спецыфичным для allauth переменным относятся те, что начинаются с ACCOUNT.
Вот переменная ACCOUNT_EMAIL_VERIFICATION имеет значение none, что в переводе
озачает следующее: проверка mail - отсутствует.
Значение именно этой переменной нам и нужно изменить.
Эта переменная может принемать и другие значения:
• mandatory - не пускать пользователя на сайт до момента подтверждения почты.
• optional - сообщение о подтверждении почты будет отправлено, но пользователь
    может залогиниться на сайте без подтверждения почты
-------------------
Заменим значение этой переменной в настройках на mandatory
django_d4/settings.py

ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
-------------------
Теперь пройдём регистрацию
------
После регистрации получим сообщение "Письмо с подтверждением регистрации было
отправлено на почту", теперь нужно зайти на почту и завершить регистрацию.
------
На почте нас ждёт два письма. Первое мы получаем как администратор, второе -
запрос подтверждения почты. В запрсе ссылка на подтверждение.
------
При нажатии на ссылку откроется наш сайт с кнопкой ( Confirm )
------
После нажатия на кнопку ( Confirm ) мы будем перенаправлены на страницу входа с
сообщением об успешном подтверждении почтового адреса.
-------------------
Параметры настройки allauth
• ACCOUNT_CONFIRM_EMAIL_ON_GET = True # позволит избежать дополнительного входа
        и активирует аккаунт сраз, как только мы перейдём по ссылке.
• ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS - Хранит количество дней, когда
        доступна ссылка на подтверждение регистрации.
---------------------------------------
Изменим шаблон посылаемого на почту письма
Создадим файл:
Путь до файла очень похож на то, как размещён шаблон в проекте.

templates/account/email/email_confirmation_message.txt

{% extends "account/email/base_message.txt" %}
{% load account %}
{% load i18n %}

{% block content %}{% autoescape off %}{% user_display user as user_display%}
{% blocktrans with site_name=current_site.name site_domain=current_site.domain%}
Вы получили это сообщение, потому что пользователь {{ user_display }}
указал этот email при регистрации на сайте{{ site_domain }}.

Для подтверждения регистрации пройдите по ссылке {{activate_url}}

Хорошего дня!
{% endblocktrans %}{% endautoescape %}
{% endblock content %}

-------------------
• templates - наша стандартная папка с шаблонами, именно в ней шаблонизатор
                Django будет искать файлы
• account\email - стандартная папка для размещения файлов, к которым обращается
                    django-allauth при формировании вертификационных писем
• email_confirmation_message.txt - сам шаблон письма, который будет
                    искать django-allauth.

Все эти шаблоны можно переписать
---------------------------------------
Создание списка рассылок                               Создание списка рассылок
---------------------------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Интерфейс подписки на рассылки

Чтобы хранить список категорий, на которые подписан пользователь, нужна новая
таблица в БД.
Добавим дляя этого модель Subscriptions.

simpleapp/models.py

from django.contrib.auth.models import User

class Subscriptions(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             related_name='subscriptions')
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE,
                                 related_name='subscriptions')
-------------------
После добавления модели нужно создать и выполнить миграцию.
-------------------
Если мы пойдём старым методом использования дженериков, понадобится несколько
представлений: вывести список, добавить подписку, удалить подписку.
Поприбуем обойтись одним представлением.
simpleapp/views.py

from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import Product, Subscriptions, Category

@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriptions.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriptions.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriptions.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )
-------------------
Вот такое представление у нас получается.
Его могут использовать только зарегистрированные пользователи. Для этого мы
использовали декоратор @login_required.
А также с помощью декоратора @csrf_protect у нас будет автоматически
проверяться CSRF-токен в получаемых формах.
    В представлении можем применять как GET, так и POST запросы.
• GET - будет выполняться когда пользователь просто открывает страницу подписок
• POST - когда пользователь нажмёт кнопку подписки или отписки от категории.
--------
    Далее по коду мы делаем не простой запрос в БД. Мы собираем все категории
товаров с сортировкой по алфавиту и добавляем спец-поле, которое покажет,
подписан сейчас пользователь на данную категорию или нет.
--------------------------------------------------------
ЭТОТ КОД ПИСАТЬ НЕ НУЖНО:
Вот так будет выглядеть запрос в SQL (этот код приведён для тех, кто
разбирается в SQL):

SELECT "simpleapp_category"."id",
       "simpleapp_category"."name",
       EXISTS
    (SELECT (1) AS "a"
    FROM "simpleapp_subscription" U0
    WHERE (U0."category_id" = ("simpleapp_category"."id")
           AND U0."user_id" = 16)
    LIMIT 1) AS "user_subscribed"
FROM "simpleapp_category"
ORDER BY "simpleapp_category"."name" ASC
-------------------------------------------------------
Запросы (query) которые вы пишете в Django, можно вывести в консоль с помощью
функции print()

print(Category.objects.all().query)
SELECT "simpleapp_category"."id", "simpleapp_category"."name" FROM "simpleapp_category"

После сбора данных из базы мы просто выводим все категории товаров с подписками
 пользователя.
-------------------
Добавим новое представление в список url:
simpleapp/urls.py

from .views import (
    ProductsList, ProductDetail, ProductsForm, ProductCreate,
    ProductUpdate, ProductDelete, subscriptions,
)

path('subscriptions/',subscriptions, name='subscriptions')
-------------------
Теперь подписки у нас будут доступны по пути /products/subscriptions/.
Для учебного проекта это не плохо.
Но в рабочих проектах нужно будет больше задумываться над тем, насколько
правильно у нас построено приложение.
    Может. Для подписок лучше было сделать отдельное Django-приложение?
Если подписки будут только на товары, и других видов уведовлений для
пользователей не будет, то подписки могут жить в этом приложении.
    В решении таких вопросов поможет только опыт и понимание задач продукта,
который вы разрабатываете.
-------------------
Создадим шаблон:
templates/subscriptions.html

{% extends 'flatpages/default.html' %}

{% block title %}
Subscriptions
{% endblock title %}

{% block content %}
    {% for category in categories %}
        <p>
            {{ category.name }}
            <form method="post">
                {% csrf_token %}
                <input type="hidden" name="category_id"
                       value="{{ category_id }}" />

                {% if category.user_subscribed %}
                    <button disabled>Подписаться</button>
                    <button name="action" value="unsubscribe">Отписаться</button>
                {% else %}
                    <button name="action"
                            value="subscribe">Подписаться</button>
                    <button disabled>Отписаться</button>
                {% endif %}
            </form>
        </p>
    {% endfor %}
{% endblock content %}
-------------------
Для каждой категории мы выводим две кнопки: подписаться и отписаться.
С помощью аргумента кнопки disabled в HTML делаем её неактивной. Пользователь
не сможет нажать на отписатся пока не подпишется.
С помощью спец-инпута с типом hidden мы говорим браузеру передать вместе с
формой id категории.
    После нажатия на кнопку подписки форма отправится, и страница обновится.
---------------------------------------
Сигналы                                                                Сигналы
---------------------------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Реализуем механизм отправки на почту уведомлений о новых товарах.
    Если решать эту задачу в лоб, то можно пойти в дженерик создания товара и
от туда отправить письма. Но товар у нас можно создать и из панели
администратора. Понимаете в чём проблема?
Чем больше мест для работы с моделью, тем больше вероятность что-то упустить.
    Для решения нашей задачи отлично подойдут сигналы.
Это такие объекты, которые могут выполнить указанные нами функции при
опредилёных событиях в приложении, например, создание или удаление объекта
модели.
Для начала посмотрим на несколько стандартных сигналов Django.

• django.db.models.signals.pre_save - выполняется до вызова save() метода
    модели
• django.db.models.signals.post_save - выполняется после вызова save() метода
    модели
• django.db.models.signals.pre_delete - выполняется до вызова delete() метода
    модели или набора объектов (queryset)
• django.db.models.signals.post_delete - выполняется после вызова метода
    модели или набора объектов (queryset)
• django.db.models.signals.m2m_changed - вызывается когда ManyToManyField в
    модели изменяется
• django.core.signals.request_started - вызывается перед обработкой
    HTTP-запроса
• django.core.signals.request_finished - вызывается после обработки
    HTTP-запроса
Остальные стандартные сигналы здесь:
https://docs.djangoproject.com/en/4.0/ref/signals/#post-save
---------------------------------------
Некоторые пакеты, которые вы устанавливаете из PyPi, могут дополнить список
своиси сигналами.
Приложение allauth добавляет в прокт внушительный список новых сигналов.
Подробнее здесь:
https://django-allauth.readthedocs.io/en/latest/account/signals.html?
highlight=allauth.account.signals.user_signed_up#signals
---------------------------------------
Сделаем функцию которая будет выполняться при создании объекта модели Products
Создадим файл signals.py

simpleapp/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product


@receiver(post_save, sender=Product)
def product_created(instance, **kwargs):
    print('Создан товар', instance)
--------------------
Просто так сигналы неначнут работать. Нам нужно выполнить этот модуль (файл с
Python-клдом). Для этого подойдёт авто-зозданный файл apps.py в нашем
приложении. В этом файле есть класс с насройками нашего приложения. Добавим в
него метод ready, который выполнится при завершении конфигурации нашего
приложения simpleapp. В самом методе импортируем сигналы, таким образом
зарегистрировав их.

simpleapp/apps.py

from django.apps import AppConfig

class SimpleappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'simpleapp'

    def ready(self):
        from . import signals  # выполнение модуля -> регистрация сигналов
--------------------
Теперь создаём товар в admin панели.
В КОНСОЛЕ увидим ообщение о создании товара и название созданного товара.
Поробнее здесь:
https://docs.djangoproject.com/en/4.0/ref/signals/#post-save

Метод save вызывается даже тогда, когда мы просто будем изменять информацию о
товаре.
Исправим это дальше.
---------------------------------------
Для отправки сообщений всем пользователям, подписавшимся на обновления в этой
категориии.
Изменим код в:

simpleapp/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
# -----------
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives


@receiver(post_save, sender=Product)
def product_created(instance, created, **kwargs):
    if not created:
        return

    emails = User.objects.filter(
        subscriptions__category=instance.category
    ).values_list('email', flat=True)
    subject = f'Новый товар в категории {instance.category}'

    text_content = (
        f'Товар: {instance.name}\n'
        f'Цена: {instance.price}\n'
        f'Ссылка на товар: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Товар: {instance.name}<br>'
        f'Цена: {instance.price}<br><br>'
        f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
        f'Ссылка на товар</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
--------------------
Как видно мы сформировали два сообщения одно с текстом, другое с HTML.
После чего отправляем письма пользователю, не забываем подписаться.
--------------------
Тестировать такой код лучше с печатью писем в консоль.
Для этого в настройках проекта укажем
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
Если использовать реальную почту, почтовый сервер может посчитать вас спамером
и прислать вот такую ошибку:

SMTPDataError at/admin/simpleapp/product/add

Вот что про это пишет Яндекс:

Если вы получили сообщение об ошибке «Письмо не может быть отправлено, потому
что кажется похожим на спам» («Spam limit exceeded» или
«Message rejected under suspicion of SPAM») или требование ввести контрольные
цифры, это могло произойти по следующим причинам:

рассылаются однотипные или шаблонные письма;
достигнуто ограничение на отправку писем в сутки;
ваш аккаунт кажется подозрительным;
отправляются письма на несуществующие адреса;
нам поступили жалобы на рассылку писем с вашего адреса.
Если это произошло, отправка писем из вашего почтового ящика будет
заблокирована. Блокируется только отправка писем — входить в Почту и получать
письма вы сможете. Блокировка закончится автоматически через 24 часа, если вы
не попытаетесь отправить письмо в течение этого времени, — иначе блокировка
продлится ещё на 24 часа.
    Ситуация неприятная, поэтому для разработки пишем в консоль.
Когда убедились, что всё ок, и нужно опробовать конечный вариант, можно
проверить на реальном почтовом сервере.
---------------------------------------
Выполнение задач по расписанию                  Выполнение задач по расписанию
---------------------------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Переодические задачи - это код, который выполняется через определённый период
времени.
Иногда переодические задачи называют "запускаемыми по cron'y".
Cron - это программа в UNIX - системах, которая переодически запускает
указанные команды. Поэтому иногда, хоть это и не очень правельно, используют
такую формулеровку.
---------------------
Плюс у этой программы есть спец-синтаксис описание переодичности выполнения
команд. Например задача может выполняться:
• раз в минуту (*****)
• в пять минут каждого часа (5****)
• каждый день в 12:34 (34 12 ***)
• каждый вторник в 23:01 (1 23 ** 1)
• в 02:01 каждого 3 апреля (1 2 3 4 *)  так далее.
---------------------
Подробнее здесь:
https://ru.wikipedia.org/wiki/Cron
https://tproger.ru/translations/guide-to-cron-jobs
---------------------------------------
Шаблон задания для Cron выглядит примерно так:
Минуты(0-59) Часы(0-24) День(1-31) Месяц(1-12) День недели(0-6) Команда
---------------------------------------
Наша задача состоит в том, чтобы переодически отправлять письма менеджерам о
самых дешёвых товарах на сайте для проверки.
    Для решения этой задачи нам понадобится пакет django-apscheduler.
Этот пакет использует указание времени переодического выполнения задач
в стиле cron.
Подробнее здесь:
https://pypi.org/project/django-apscheduler/
---------------
pip install django-apscheduler

------------------
Зарегистрировал в settings
django_apschedulerv

Добавил в settings

APSCHEDULER_DATETIME_FORMAT = 'N j, Y, f:s a' # формат даты
APSCHEDULER_RUN_NOW_TIMEOUT = 25 # продолжительность выполнения 25 сек.
------------------
Это приложение использует модели, поэтому нужно выполнить миграции для создания
таблиц в БД
python manage.py makemigrations
python manage.py migrate
---------------
Тепреь как написанно в документации, создадим свою джанго-команду для
выполнения переодических задач.
    Путь до файла с командой очень важен. Файл должен лежать в одном из наших
приложений, по пути management/commands.
А название файла будет идентично тому как мы хотим назвать КОМАНДУ.
---------------
Получается при создании файла
simpleapp/management/commands/runapscheduler.py у нас станет доступна команда
python manage.py runapscheduler.
---------------
Создалим файл:
simpleapp/management/commands/runapscheduler.py

import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

logger = logging.getLogger(__name__)

def my_job():
    pass

@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    Это задание удаляет записи выполнения заданий APScheduler старше
    максимального возраста 'max_age' из БД.
    Это помогает предотвратить заполнение БД старыми историческими данными,
    записи которые больше не нужны.
    : param max_age: максимальная продолжительность хранения исторических
    записей выполнения заданий. По умолчанию 7 дней.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'ny_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
---------------
Теперь заменим код my_job на отправку сообщений менеджерам.
simpleapp/management/commands/runapscheduler.py

import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import mail_managers
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from simpleapp.models import Product

logger = logging.getLogger(__name__)


def my_job():
    print("DOROTY DAUN")
    products = Product.objects.order_by('price')[:3]
    text = '\n'.join(['{} - {}'.format(p.name, p.price) for p in products])
    mail_managers("Самые дешёвые товары", text)


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    Это задание удаляет записи выполнения заданий APScheduler старше
    максимального возраста 'max_age' из БД.
    Это помогает предотвратить заполнение БД старыми историческими данными,
    записи которые больше не нужны.
    : param max_age: максимальная продолжительность хранения исторических
    записей выполнения заданий. По умолчанию 7 дней.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/30"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
---------------
Запустим:
python manage.py runserver
откроем второе окно терминала и введём команду для запуска выполнения
задач по расписанию:
python manage.py runapсsheduler
---------------
Получим письмо на почту
Для тестировки приложения можно использовать print()

def my_job():
    print("DOROTY DAUN")
В терминале по расписанию будет выводиться DOROTY DAUN
---------------------------------------
D_7                                                                        D_7
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Синхронное и асинхронное взаимодействие
------------
Синхронное - При синхронном взаимодействии Клиент отправляет Серверу запрос
(например, загрузить файл). Сервер принемает этот запрос, обрабатывает его и
выдаёт ответ. В это время Клиент блокируется - никакие другие запросы он
выполнить не может до получения ответа с Сервера на предыдущий запрос.
    Такой тип взаимодействия называют блокирующим.
Кажется что у такого типа взаимодействия много недостатков, но несмотря на это
он используется довольно часто.И это не удивительно, ведь наш процесс мышления
в своей основе тоже работает по синхронном принципу. Все входящие «запросы» и
исходящие «ответы» находятся в одном потоке сознания. Оно обладает фокусом
внимания, которое позволяет концентрироваться на определенных действиях.
Конечно, здесь можно возразить, что человек иногда способен выполнять множество
действий одновременно, но это лишь благодаря способности нашего мозга быстро
переключаться между задачами, что создает эффект многопоточности.
------------
Асинхронное - Другой тип взаимодействия называется асинхронным. Его ещё
называют неблокирующим, потому что в момент выполнения запроса Клиент может
продолжать работу - посылать запросы на сервер и принимать ответы вне
зависимости от того, в каком состоянии сейчас находится сервер.
    Асинхронность работы Клиента и Сервера обеспечивает большую
производительность, т. к. минимизируются потери времени на передачу запроса и
получение ответа (клиент в это время не блокируется). Кроме того, как
следствие — более высокая стабильность работы, ведь неполадки на одной из
сторон не так сильно влияют на другую. Плата за такие очевидные и сильные
плюсы — более сложная разработка.
        Основной компонент асинхронного взаимодействия - это очередь сообщений.
------------
Этот компонент выступает как бы в роли посредника между Клиентом и Сервером.
Клиент, отправляя запрос, помещает задачу в очередь, а сам в то время продолжает
работу. Сервер же постоянно «мониторит» очередь на наличие сообщений — запросов,
которые нужно выполнить, и обрабатывает их. Здесь, кстати, можно вспомнить модуль,
посвященный алгоритмам и структурам данным, на котором мы разбирали очередь
(queue) как абстрактную структуру.
---------------------------------------
Библиотека Celery
------------
Для использования асинхронного взаимодействия в Django-проектах проверенным
временем решением является библиотека Celery.
------------
Устанавливаем Celery.

pip install celery
------------
Далее, согласно документации библиотеки, необходимо перейти в директорию
проекта и создать файл celery.py рядом с settings.py
django_d4/django_d4/celery.py
------------
celery.py

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'simpleapp.settings')

app = Celery('simpleapp')
app.config_from_object('django.conf:settings',
                       namespace='CELERY')
app.autodiscover_tasks()
------------
• В первую очередь мы импортируем библиотеку для взаимодействия с операционной
    системой и саму библиотеку Celery.
• Второй строчкой мы связываем настройки Django с настройками Celery через
    переменную окружения.
• Далее мы создаем экземпляр приложения Celery и устанавливаем для него файл
    конфигурации. Мы также указываем пространство имен, чтобы Celery сам
    находил все необходимые настройки в общем конфигурационном файле
    settings.py. Он их будет искать по шаблону «CELERY_***».
• Последней строчкой мы указываем Celery автоматически искать задания в файлах
    tasks.py каждого приложения проекта.
------------
Также, согласно рекомендациям из документации к Celery, мы должны добавить
следующие строки в файл __init__.py (рядом с settings.py):
__init__.py

from .celery import app as celery_app

__all__ = ('celery_app',)

На этом базовые настройки Celery окончены.
---------------------------------------
Брокеры сообщений
---------------------------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Если мы используем асинхронный подход взаимодействия различных компонентов
проекта или для связи Клиента и Сервера, необзодим эффективный способ хранения
очереди сообщений и их передачи между компонентами.
Это реализуют Брокеры Сообщений.
    Основная их задача - хранение (и возможно преобразование) сообщений от
источника сообщений (обычно его называют producer), которые могут брать на
обработку оработчики этих сообщений (consumer).
    Ситуация становится еще более интересной, когда у нас есть несколько
источников сообщений и/или несколько обработчиков. Такая ситуация как раз
наблюдается в веб-приложениях, когда много пользователей одновременно
отправляют сложные для обработки запросы на сервер. Возникает потребность
каким-то эффективным образом их организовать, чтобы не потерять задачи и не
проиграть в производительности их выполнения.
    Необходимый функционал, хорошо совместимый с Celery,
  реализуют Redis и RabbitMQ
---------------------------------------
RabbitMQ
---------------------------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Обмен сообщениями сам по себе не является сложной задачей, но ему сопутствуют
требования, которым он должен удовлетворять:
• эфективность
• отказоустойчивость
• стабильность
Для этого был создан протокол AMQP — Advanced Message Queuing Protocol.
В протоколе AMQP существует три основных понятия:
• обменник (exchange)
• очередь (queue)
• маршрут (routing key)

Источник сообщения передаёт задачи в RabbitMQ, где они всегда сначала попадают
в обменник. Он, в зависисмости от типа задачи (ключа маршрутизаии), опредиляет
одну или несколько очередей, в которые может попасть эта задача. С другой
стороны, каждая очередь сама вызывает тот или иной обработчик (consumer) для
выполнения задач из очереди.
    Внутри RabbitMQ имеет свою базу данных, оптимизированную под эти задачи,
но в первую очередь — это полноценный сервер очередей. Это его основная цель.
RabbitMQ — достаточно популярный брокер сообщений и часто используется в
больших проектах.
---------------------------------------
Redis
---------------------------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Второй вариант работы с очередями - это Redis
В отличие от RabbitMQ, сам по себе он не является сервером очередей.

Redis - это размещаемая в памяти база данных типа «ключ-значение».
    Главное отличие Redis от более классических баз данных в том, что вся
информация хранится в оперативной памяти, а не на диске. У таких баз все данные
(таблицы, например) хранятся в виде файлов на самом диске. Redis предпочитает
все хранить в оперативной памяти и только периодически делает «снимки» данных
на диск для сохранения целостности. И это дает свой отличный бонус — скорость
работы такой базы данных.
------------
Redis поддерживает несколько типов данных в виде значения.
• строки
• числа
• двоичные последовательности
• хеш-таблицы (они же словари)
• списки (структура данных)
• множества и даже сортированные множества и др.
------------
Как мы уже вспоминали, очередь — это структура данных, работающая по принципу
 First-In First-Out (FIFO). И ее можно реализовать на списках, которые как раз
поддерживаются Redis!
• FIFO - первым зашёл первым вышел
• LIFO - первым зашёл последним вышел

подробнее здесь
Шпаргалка по Redis:  https://habr.com/ru/articles/204354/
------------
В нем есть какое-то количество каналов (channel) — это и есть пара
«ключ-значение», где ключом выступает имя канала (известное как источнику, так
и обработчику), а значение — это очередь сообщений. Источник сообщений
(или несколько) публикует сообщения в каналы. В свою очередь обработчики
сообщений (условно, подписчики канала) постоянно мониторят каналы на наличие
сообщений и в случае необходимости забирают их на обработкумВ нем есть какое-то
количество каналов (channel) — это и есть пара «ключ-значение», где ключом
выступает имя канала (известное как источнику, так и обработчику),
а значение — это очередь сообщений. Источник сообщений (или несколько) публикует
сообщения в каналы. В свою очередь обработчики сообщений
(условно, подписчики канала) постоянно мониторят каналы на наличие сообщений и
в случае необходимости забирают их на обработку
Можно заметить некоторую нестыковку понятий. Дело в том, что есть два немного
разных подхода — очередь сообщений и издатель/подписчик. Их еще называют
шаблонами проектирования. С помощью Redis можно реализовать оба подхода.
Между ними есть принципиальные отличия, но они для нас сейчас несущественны,
ведь надо понять, как работает система в целом.
    Redis может использоваться не только как очередь сообщений. Область ее
применения очень широкая.
Подробнее здесь: https://habr.com/ru/companies/manychat/articles/507136/
--------------
Установка Redis
--------------------------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Для установки Redis нужно выполнить следующие команды в терминале:

$ sudo add-apt-repository ppa:redislabs/redis
$ sudo apt-get update
$ sudo apt-get install redis
-------------------------------
Удостовериться в том, что Redis установлен, можно с помощью команды:

$ redis-cli ping
Эта команда, в случае успеха, должна вернуть PONG. Обычно сразу после установки
сервер Redis запускается самостоятельно, но если это не произошло, то можно
запустить его следующей командой:

$ redis-server
Далее нам нужно настроить поддержку Redis в Python и Celery. Вновь зайдите в
виртуальное окружение и установите следующие пакеты:

(virtualenv) $ pip3 install redis
(virtualenv) $ pip3 install -U "celery[redis]"
------------------------
Если вы устанавливаете его на Windows, то вам поможет облачный сервис от
Redislabs, с помощью которого вы будете хранить ваши данные в облаке. Нужен VPN
---------------------
Установил на комп
Папка Redis

Сначала запускаем- redis-server
Затем запускаем- redis-cli
Работает
----------------------
Далее мы должны добавить некоторые настройки в конфигурацию проекта
(settings.py), дописав следующие строки:

settings.py

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

------------
• CELERY_BROKER_URL — указывает на URL брокера сообщений (Redis). По умолчанию
    он находится на порту 6379.
• CELERY_RESULT_BACKEND — указывает на хранилище результатов выполнения задач.
• CELERY_ACCEPT_CONTENT — допустимый формат данных.
• CELERY_TASK_SERIALIZER — метод сериализации задач.
• CELERY_RESULT_SERIALIZER — метод сериализации результатов.
---------------------------------------

---------------------------------------
django_d4/celery.py

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'django_d4.settings')

app = Celery('django_d4')
app.config_from_object('django.conf:settings',
                       namespace='CELERY')
app.autodiscover_tasks()
-----------------------------
Если вы используете Redis Labs, то переменные CELERY_BROKER_URL и
CELERY_RESULT_BACKEND должны строиться по шаблону:

redis://логин:пароль@endpoint:port
где endpoint и port вы также берёте из настроек Redis Labs.

Также обратите внимание, что Celery с версией выше 4+ не поддерживается Windows.
Поэтому если у вас версия Python 3.10 и выше, запускайте Celery, добавив в
команду флаг: --polo=solo.

celery -A django_d4 worker -l INFO --pool=solo
--------------
И, наконец, попробуем запустить локальный сервер Django и Celery. Для этого вы
должны иметь два окна терминала. В одном из них, как и обычно,
вы должны запустить Django:

python3 manage.py runserver
-----------------
А в другом — запустить Celery:

celery -A django_d4 worker -l INFO --pool=solo
-----------------
Получим такой результат:

 -------------- celery@DESKTOP-IH4T6KH v5.3.4 (emerald-rush)
--- ***** -----
-- ******* ---- Windows-10-10.0.19045-SP0 2023-10-16 11:18:28
- *** --- * ---
- ** ---------- [config]
- ** ---------- .> app:         django_d4:0x240a06df310
- ** ---------- .> transport:   redis://localhost:6379//
- ** ---------- .> results:     redis://localhost:6379/
- *** --- * --- .> concurrency: 4 (solo)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** -----
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery
--------------
Это указывает нам на то, что Celery успешно запущен, может принимать и о
брабатывать задачи. И более того видно, что он использует Redis в качестве
«transport» — брокера сообщений. Well done!
---------------------------------------
Создание задач
---------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Базовой структурной единицей системы Celery является task (задача) ( — таска).

нас есть еще брокер, который хранит задачи. Также у нас есть
очередь — структура, в которой хранятся таски, а еще есть загадочный
worker — это часть системы, которая отправляет задачи из очереди на исполнение.
-----------------
Создание задачи
----------
Все задачи принято хранить в файлах с названием tasks.py. В таком случае Celery
сможет самостоятельно находить задачи. Любая задача представляет собой обычную
функцию с одной особенностью: она должна быть обернута в декоратор.

В Django-проектах есть удобный декоратор, которым можно воспользоваться, если
в файле __init__.py были проведены необходимые импорты. Если это было сделано,
в файле tasks.py импортируем декоратор из библиотеки:

Напишем простую задачу, которая будет выводить «Hello, world!» в консоль.
Создаём файл tasks.py
simpleapp/tasks.py

from celery import shared_task
import time

@shared_task
def hello():
    time.sleep(10)
    print("Hello World!")
--------------
использовали функцию sleep() из пакета time, чтобы остановить выполнение
процесса на 10 секунд. Это поможет нам убедиться, что Клиент не «встал», пока
выполняется эта задача.
-------------
 -------------- celery@DESKTOP-IH4T6KH v5.3.4 (emerald-rush)
--- ***** -----
-- ******* ---- Windows-10-10.0.19045-SP0 2023-10-17 13:44:45
- *** --- * ---
- ** ---------- [config]
- ** ---------- .> app:         django_d4:0x22336ae3310
- ** ---------- .> transport:   redis://localhost:6379//
- ** ---------- .> results:     redis://localhost:6379/
- *** --- * --- .> concurrency: 4 (solo)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** -----
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery


[tasks]
  . simpleapp.tasks.hello    #  Вот это сообщение
--------------
ВАЖНО: после каждого изменения кода задач необходимо перезагружать Celery.
Он не умеет автоматически обнаруживать изменения кода.
--------------
Проверим работоспособность. Добавим путь
simpleapp/urls.py

from .views import (
    ProductsList, ProductDetail, ProductsForm, ProductCreate,
    ProductUpdate, ProductDelete, subscriptions,  IndexView
)

path('index/', IndexView.as_view()),
---------------
Добавим представление:

simpleapp/views.py

from django.http import HttpResponse
from django.views import View
from .tasks import hello

class IndexView(View):
    def get(self, request):
        hello.delay()
        return HttpResponse('Hello!')
-----------------
Будет доступно по адресу:
http://127.0.0.1:8000/products/index/
---------
В браузере будет натпись Hello!!!!
обновление каждые 10 сек.
----------------
Здесь мы использовали класс-представление. В методе get() мы написали
действия,
которые хотим выполнить при вызове этого представления — выполнить задачу
hello (метод delay() обсудим чуть позже) и вернуть только 'Hello!' в браузер.
---------------
После чего зайдите в консоль Celery и вы увидите вывод «Hello, world!» через 10
секунд после каждой загрузки страницы. Чтобы убедиться, что работа сайта не
останавливается на каждые 10 секунд, перезагрузите страницу множество раз. И
после этого еще раз посмотрите в консоль Celery.
-----
Например, если 5 раз подряд открыть эту страницу, то будет создано 5 задач
«hello», но каждая со своим идентификатором (длинный набор букв и цифр). А
после чего они все начнут выполняться в соответствии с тем временем, на которое
мы «заморозили» задачу.
---------------------------------------
Вызов задач
---------------------------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
В данном примере для вызова задачи мы использовали метод delay()
Есть два метода для того, чтобы сделать это:

apply_async(args[, kwargs[, ...]])
delay(*args, **kwargs)

Но на самом деле это один и тот же метод! Метод delay() — это сокращение для
метода apply_async(), позволяющее вызвать его с меньшим количеством кода.
Метод apply_async(), в свою очередь, открывает больше возможностей.

Представим, что у нас есть задача, которая зависит от аргументов. Например,
сделаем цикл, который раз в секунду печатает число от 1 до переданного числа:

Добавим задачу в:
tasks.py

@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)
----------
Перезагрузим celery
В консоле получим результат

[tasks]
  . simpleapp.tasks.hello
  . simpleapp.tasks.printer
--------------
Добавим теперь эту задачу в views.py
simpleapp/views.py

from .tasks import hello, printer

class IndexView(View):
    def get(self, request):
        printer.delay(10)
        hello.delay()
        return HttpResponse('Hello!!!!')
--------------
Выполнение этого представления приведет к следующему выводу в консоли Celery:
[2023-10-17 14:19:40,308: WARNING/MainProcess] 1
[2023-10-17 14:19:41,323: WARNING/MainProcess] 2
[2023-10-17 14:19:42,332: WARNING/MainProcess] 3
[2023-10-17 14:19:43,336: WARNING/MainProcess] 4
[2023-10-17 14:19:44,347: WARNING/MainProcess] 5
[2023-10-17 14:19:45,357: WARNING/MainProcess] 6
[2023-10-17 14:19:46,367: WARNING/MainProcess] 7
[2023-10-17 14:19:47,375: WARNING/MainProcess] 8
[2023-10-17 14:19:48,384: WARNING/MainProcess] 9
-------------
 Нам необходимо было передать аргумент в функцию-задачу. Для этого мы передали
 нужный аргумент в метод delay() и все! Никаких сложных схем. Можно передавать
 необходимое количество аргументов как напрямую, так и именованных.
 Иными словами, вызвать задачу можно было бы и так:
printer.delay(N = 10)

Метод delay() забирает все аргументы и передает их в функцию, ничего не
оставляя себе . Как мы уже сказали, delay() маскирует apply_async().
Пример из документации показывает, как они связаны.

Например, если мы вызываем:

task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
на самом деле вызывается:

task.apply_async(args=[arg1, arg2],
                 kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
---------------------------------------
apply_async   Три дополнительных параметра выполнения:
--------------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
• countdown - устанавливает время (в секундах), через которое задача должна
    начать выполняться
-----------
Укажем, что задача счетчика должна начаться через 5 секунд после того,
как она была создана:
Изменим представление

simpleapp/views.py

class IndexView(View):
    def get(self, request):
        printer.apply_async([10], countdown=5)
        hello.delay()
        return HttpResponse('Hello!!!!')
---------------
Перезагрузим celery
Перезагрузим страницу в браузере
Получим результат в консоле
[2023-10-17 14:31:18,516: WARNING/MainProcess] 1
[2023-10-17 14:31:19,526: WARNING/MainProcess] 2
[2023-10-17 14:31:20,538: WARNING/MainProcess] 3
[2023-10-17 14:31:21,551: WARNING/MainProcess] 4
[2023-10-17 14:31:22,561: WARNING/MainProcess] 5
[2023-10-17 14:31:23,199: WARNING/MainProcess] Hello World!
[2023-10-17 14:31:23,201: INFO/MainProcess] Task simpleapp.tasks.hello[b214b3f6-0cc3-42bd-babc-b
0fc6b0c4f7b] succeeded in 10.015999999974156s: None
[2023-10-17 14:31:23,564: WARNING/MainProcess] 6
[2023-10-17 14:31:24,575: WARNING/MainProcess] 7
[2023-10-17 14:31:25,583: WARNING/MainProcess] 8
[2023-10-17 14:31:26,599: WARNING/MainProcess] 9
[2023-10-17 14:31:27,610: WARNING/MainProcess] 10
---------------------------------------
• eta - Если countdown принимает целое число (количество секунд), то параметру
    eta требуется уже объект типа datetime.
    Например, для реализации того же самого сдвига на 5 секунд мы можем
получить текущее время и добавить timedelta, равное 5 секундам, чтобы получить
datetime-объект момента через 5 секунд от текущего.

-----------------
Если datetime не работает тогда делаем так:
from datetime import timedelta
from django.utils import timezone
----------------
views.py

from datetime import datetime, timedelta
from django.utils import timezone

class IndexView(View):
    def get(self, request):
        printer.apply_async([10],
                            eta = datetime.now() + timedelta(seconds=5))

        #  printer.apply_async([10], eta=timezone.now() + timedelta(seconds=5))

        hello.delay()
        return HttpResponse('Hello!')
--------------
В полях моделей Django есть дата/время, которые очень легко
преобразуются в datetime-объекты.

---------------------------------------
• expires- служит для того, чтобы убирать задачу из очереди по прошествии
    какого-то времени.
Такое иногда бывает необходимо в тех случаях, когда выполнение задачи
становится уже не актуальным.
    Необходимо иметь автоматизированную «чистку» таких задач. И для этого нам
нужен как раз expires, который принимает datetime-объект или число. Первый
вариант указывает на точное время, когда задача должна быть убрана из очереди,
а второй — число, количество секунд, через которое задачу нужно убрать.
---------------------------------------
Не делал Добавил как пример:
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Продемонстрируем работу брокера сообщений на примере «доски» заказов McDonalds.

Что мы имеем? Модели Product, Order и промежуточная модель ProductOrder:

board/models.py

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length = 255)
    price = models.FloatField(default = 0.0)

    def __str__(self):
        return self.name + "/" + str(self.price)

class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add = True)
    time_out = models.DateTimeField(null = True)
    cost = models.FloatField(default = 0.0)
    take_away = models.BooleanField(default = False)
    complete = models.BooleanField(default = False)

    products = models.ManyToManyField(Product, through = 'ProductOrder')

class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    amount = models.IntegerField(default = 1)
-------------
Имеем также конфигурацию URL:

board/urls.py

from django.urls import path
from .views import IndexView, NewOrderView, take_order

urlpatterns = [
    path('', IndexView.as_view()),
    path('new/', NewOrderView.as_view(), name = 'new_order'),
    path('take/<int:oid>', take_order, name = 'take_order')
]
------------
И соответствующие им представления:

from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView
from .tasks import complete_order
from .models import Order
from datetime import datetime

# главная страница - таблица заказов
class IndexView(TemplateView):
    template_name = "board/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.all()
        return context

# форма нового заказа
class NewOrderView(CreateView):
    model = Order
    fields = ['products'] # единственное поле
    template_name = 'board/new.html'

    # после валидации формы, сохраняем объект,
    # считаем его общую стоимость
    # и вызываем задачу "завершить заказ" через минуту после вызова
    def form_valid(self, form):
        order = form.save()
        order.cost = sum([prod.price for prod in order.products.all()])
        order.save()
        complete_order.apply_async([order.pk], countdown = 60)
        return redirect('/')

# представление для "кнопки", чтобы можно было забрать заказ
def take_order(request, oid):
    order = Order.objects.get(pk=oid)
    order.time_out = datetime.now()
    order.save()
    return redirect('/')
------------
И, наконец, наша единственная задача, которая только ставит
True на флаг завершенности заказа.
--------!!!!!!!!!!!!---------
ВАЖНО: Для обеспечения эффективности работы не рекомендуется передавать объекты
моделей напрямую в аргумент задачи. Ведь он тогда должен будет полностью
храниться в памяти в сериализованном виде, а это сложно и долго
(для самого Python). Поэтому рекомендуется передавать ID объектов или
параметры, по которым можно определить один или несколько объектов, к которым
должна примениться эта функция.
-------------
board/tasks.py

from celery import shared_task
from .models import Order

@shared_task
def complete_order(oid):
    order = Order.objects.get(pk = oid)
    order.complete = True
    order.save()
--------------
У нас есть также несколько шаблонов:

main.html

<html>
    <head>
        <title> Order board</title>
    </head>
    <body>
        <div>
            <h1><a href="/">Order board</a></h1>
        </div>
        <div>
            <button>
                <a href="{% url 'new_order'%}"> Добавить заказ </a>
            </button>
        </div>
        {% block content %}
        {% endblock %}
    </body>
</html>
-------------
В основном шаблоне мы определили блок content, а также кнопку
«Добавить заказ», которая переадресует пользователя на страницу с формой.
От этого шаблона также наследуется шаблон главной страницы:

board/index.html

{% extends "main.html" %}

{% block content %}
<table>
    <thead>
    <tr>
        <th>Номер заказа</th>
        <th>Стоимость</th>
        <th>Заказ оформлен</th>
        <th>Статус</th>
    </tr>
    </thead>

    {% for order in orders %}
    <tr>
        <th>{{ order.id }}</th>
        <th>{{ order.cost }}</th>
        <th>{{ order.time_in|time:"H:i" }}</th>
        <th>{% if not order.complete %}
             Заказ еще не готов.
            {% elif order.time_out is None %}
            <button><a href="{% url 'take_order' order.id %}"> Забрать </a></button>
            {% else %}
            Заказ забрали {{ order.time_out|time:"H:i" }}
            {% endif %}
        </th>

    </tr>
    {% endfor %}
</table>

{% endblock %}
----------
Здесь мы в цикле печатаем строчки таблицы с заказами. В последнем столбце будет
три возможных варианта: «заказ еще не готов», кнопка «забрать заказ» или время
выдачи заказа.
-----------
И, наконец, простейшая форма добавления заказа:

{% extends "main.html" %}

{% block content %}
<form method="post">{% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Оформить заказ">
</form>
{% endblock %}
------------------!!!!!!!!!!!!!!!!!!!!!!!!!!!!---------------------
Дополнительные настройки Celery
---------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Celery — планирование задач.
----------
celery -A django_d4 worker -l INFO --pool=soloers

Этой командой Мы говорим Celery запустить воркер (worker)
для приложения (флаг -A означает application) с именем django_d4.
Последний флаг -l и его значение INFO указывает,
что именно выводить в лог консоли
--pool=soloers флаг добавляется для
(Также обратите внимание, что Celery с версией выше 4+ не поддерживается Windows.
Поэтому если у вас версия Python 3.10 и выше, запускайте Celery, добавив в
команду флаг: --polo=solo.)
-----------
При инициализации воркера можно также указывать количество процессов, которые
могут на нём запускаться. Это можно сделать, если указать параметр concurrency:

celery -A django_d4 worker -l INFO --concurrency=10
-----------
Настройки Celery позволяют создавать несколько воркеров, несколько очередей с
различными маршрутизациями.
Однако хочется, чтобы вы знали о существовании таких возможностей и при
необходимости сами могли обратиться к документации для знакомства с ними.
-----------
Для запуска задач по расписанию,необходимо запускать Celery с флагом -B,
который позволяет запускать периодические задачи:

celery -A django_d4 worker -l INFO -B
-----------
Для запуска периодических задач на Windows запустите в разных окнах терминала:

celery -A PROJECT worker -l INFO
и
celery -A PROJECT beat -l INFO

celery -A news_portal worker -l INFO --pool=solo

---------------------------------------
Добавление периодических заданий
----------------
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Добавление периодических заданий.
На этапе настройки Celery мы создавали файл celery.py, в котором связывали
собственную конфигурацию с конфигурацией Django.
    В этом же файле мы можем добавить и само расписание, по которому должны
будут запускаться задачи. Само расписание представляет собой словарь словарей.
Ключ основного словаря — это имя периодической задачи. Значение — это словарь
с параметрами периодической задачи — сама задача, которая будет выполняться,
аргументы, а также параметры расписания.
Пример:
---------
celery.py

app.conf.beat_schedule = {
    'action_every_30_seconds': {
        'task': 'tasks.action',
        'schedule': 30,
        'args': ("some_arg"),
    },
}
-----------
Название пункта в расписании — action_every_30_seconds. Принято давать
осмысленные названия позициям в расписании. Из собственного опыта кажется
логичным, указывать (хотя бы кратко) задачу, выполняемую периодически и,
собственно, сам период. Однако никаких жестких регламентов здесь, разумеется,
нет.

В качестве более реального, пусть и абсолютно бесполезного, примера посмотрим,
как можно запустить счетчик от 1 до N как периодическую задачу.
-----------
app.conf.beat_schedule = {
    'print_every_5_seconds': {
        'task': 'board.tasks.printer',
        'schedule': 5,
        'args': (5,),
    },
}
--------------
celery.py

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'django_d4.settings')

app = Celery('django_d4')
app.config_from_object('django.conf:settings',
                       namespace='CELERY')
app.conf.beat_schedule = {
    'print_every_5_seconds': {
        'task': 'board.tasks.printer',
        'schedule': 5,
        'args': (5,),
    },
}
app.autodiscover_tasks()
---------------
Добавим этот код в файл celery.py. Здесь мы каждые 5 секунд вызываем таску
printer, которую мы писали ранее. У нее есть аргумент (конец счетчика), и мы
его передаем в виде аргумента в ключе ‘args’. Перезапускаем Celery и
наслаждаемся бесконечным счетчиком от 1 до 5, который перезапускается
каждые 5 секунд.
---------------------------------------
crontab
---------
!!!!!!!!!!!!!!!!!!!!!!!!
crontab - позволяет задавать расписание, ориентируясь на точное время, день
            недели, месяца и т. д.
-------------
Пример              	                                 Что означает
crontab()	                                        Каждая минута
crontab(minute=0, hour=0)	                        Ежедневно в полночь
crontab(minute=0, hour='*/3')	                    Каждые три часа: 00:00, 03:00, 06:00, 09:00 и т. д.
crontab(minute=0, hour='0,3,6,9,12,15,18,21')	    Тоже самое
crontab(minute='*/15')	                            Выполнять каждые 15 минут
crontab(day_of_week='sunday')	                    Выполнять каждую минуту (!) в вокресенье
crontab(minute='*', hour='*', day_of_week='sun')	Аналогично предыдущему
crontab(minute=0, hour='*/2,*/3')	                Выполнять каждый четный час и каждый час, который делится на 3
crontab(0, 0, day_of_month='2')	                    Выполнять во второй день каждого месяца
crontab(0, 0, day_of_month='2-30/2')	            Выполнять каждый четный день
crontab(0, 0, day_of_month='11',month_of_year='5')	Выполнять только 11 мая каждого года
-------------
чтобы выполнить какую-то задачу каждый понедельник в 8 утра, необходимо
в расписание добавить следующее:

celery.py

from celery.schedules import crontab

app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'action',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (agrs),
    },
}
---------------------------------------
Также, например, есть возможность добавить «солнечный календарь», в котором по
географическим координатам можно создать расписание по времени рассвета,
заката, полудня (астрономического) и т. д.
Для этого необходимо импортировать:
----------
from celery.schedules import solar
----------
И почитать документацию:
https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html#solar-schedules
---------------------------------------
Практический пример:  McDonalds
Так случается, что заказы из McDonalds не забирают, и их нужно убирать из доски.
А также, если заказ уже забрали, то он не должен вечно висеть на доске, его
нужно убирать. В общем и целом, нам нужно оставлять только актуальные на
текущий момент заказы. Давайте сделаем периодическую задачу очистки
неактуальных заказов с доски. Для простоты будем удалять объекты модели Order.

Сначала сделаем саму задачу. На «приготовление» заказа у нас отводится одна
минута. Допустим, что заказ становится неактуальным (вне зависимости от статуса
заказа) после 5 минут на доске. Мы должны исключить (exclude метод запроса из
базы данных) из всей выборки актуальные заказы, а все оставшиеся удалить.
------------
@shared_task
def clear_old():
    old_orders = Order.objects.all().exclude(time_in__gt =
                        datetime.now() - timedelta(minutes = 5))
    old_orders.delete()
------------
И добавим эту задачу как периодическую задачу в расписании.
Будем ее выполнять каждую минуту.
------------
app.conf.beat_schedule = {
    'clear_board_every_minute': {
        'task': 'board.tasks.clear_old',
        'schedule': crontab(),
    },
}
---------
Заказы сами собой исчезли из доски. Мы им только немного помогли.
---------------------------------------
==============================================================================
Скачал с GitHab
Нужно установить:
Django
allauth
django-apscheduler
pip install celery
pip install redis
pip install -U "celery[redis]"
value
django-filter
==============================================================================
D_8                                                                      D_8
==============================================================================
Кеширование
-------------
Кеширование - это хранение часто используемых данных в более доступных метах с
 целью оптимизации и ускорения доступа к ним.
Проще говоря: там где можно было один раз сгенерировать и сохранить, а потом
отдать какие-то данные (при том мы точно знаем, что с момента генерации данные
никак не изменились), мы постоянно генерируем их по новой снова и снова,
снижая производительность нашего сервера.
-------------
Кеширование - Под этим, как правило, подразумевается простое и доступное место.
    Например, запись данных в файл, вместо генерации новых данных, тоже будет
кэшированием. Хоть файл это и медленнее, чем, скажем, оперативная память.
    Как правило, отдаваемые данные хранятся на сервере приложения, но некоторые
системы кэширования позволяют хранить данные и на устройстве пользователя,
однако Django не поддерживает именно этот способ, так как он не относится к
кэшированию на бэкэнде
-------------
Примечание. На момент написания курса актуальная версия Django — 3.1. Если у
вас более свежая версия, рекомендуем свериться с актуальной документацией.
Django’s cache framework | Django documentation | Django
https://docs.djangoproject.com/en/3.1/topics/cache/
-------------
Большое многообразие вариантов даёт пространство для маневрирования и
использования самых разнообразных способов кэширования. Оперативная память,
файловое хранилище, база данных и, наконец, можно написать даже собственный
способ хранения кэша. Также есть варианты использования уже знакомых вам
инструментов вроде Redis или rabitmq.
Для написания кэширования через сторонние приложения в виде редиса или рэбита
нужно задействовать сторонние библиотеки и подключать самих брокеров,
настраивая под них проект. В то время как способ с файловой системой является
наиболее наглядным, т. к. мы явно видим, где и как хранится наш кэш, при
минимальных изменениях в нашем приложении
-------------
Для того, чтобы добавить кэширование через файловую систему в наш проект,
достаточно выполнить несколько простых шагов:
• Добавляем в settings.py следующий словарь:
settings.py

import os

CACHES = {
    'default': {
        'BACKEND':
            'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files') # Указываем, куда
        # будем сохранять кэшируемые файлы! Не забываем создать папку
        # cache_files внутри папки с manage.py!
    }
}
-------------
• Создаём папку ту самую папку cache_files внутри
основного каталога. В папке где находится файл manage.py
django_d4/cache_files
-------------
Нужно отметить, что способы кэширования с точки зрения реализации отличаются
лишь тем, что вы указываете в settings.py, и как настраиваете средства
кэширования (создаёте ли директорию для файлового кэширования или таблицу для
кэширования в нашем случае). Всё остальное за вас сделает Django, т. е. для
любого из способов кэширования набор команд, выполняющих все операции,
полностью совпадает.
    Однако проблемы были замечены при использовании БД кэша и базы данных SQlite,
поэтому будьте осторожны при их совместном использовании! (тем не менее при
использование других СУБД неполадок замечено не было).
Первым же вариантом кэширования в документации предложено кэширование всего
сайта. Оно настраивается наиболее просто и не всегда является эффективным,
потому как есть сайты на которых надо кэшировать не полностью все страницы,
а лишь отдельные.
-------------
Если в проекте представления (views), оформленные через ФУНКЦИИ,
тогда кэширование будет выполняться очень просто.

from django.views.decorators.cache import cache_page # импортируем декоратор
для кэширования отдельного представления

@cache_page(60 * 15) # в аргументы к декоратору передаём количество секунд,
которые хотим, чтобы страница держалась в кэше. Внимание! Пока страница
находится в кэше, изменения, происходящие на ней, учитываться не будут!
def my_view(request):
    ...
-------------
Добавил в:
simpleapp/views.py

from django.views.decorators.cache import cache_page

@login_required
@csrf_protect
@cache_page(60 * 15)  # Добавил количество секунд которые хотим, чтобы
                      # страница держалась в кэше.
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        pprint(f'CATEGORY_ID = {category_id}')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')
        pprint(category)
-------------
Если используете КЛАССОВЫЕ представления или дженерики, то нужно добавлять
кэширование напрямую в urls.py (в котором хранятся именно сами представления,
а не основной urls.py из папки с settings.py).
Измеенил -
path('<int:pk>', cache_page(60*10)(ProductDetail.as_view()), name='product_detail'),
--------
simpleapp/urls.py

from django.views.decorators.cache import cache_page

urlpatterns = [

    path('<int:pk>', cache_page(60*10)(ProductDetail.as_view()),
    name='product_detail'),  # Добавил

    path('products_form/', ProductsForm.as_view()),
    path('create/', ProductCreate.as_view(), name='product_create'),
    path('<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),
    path('<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('index/', IndexView.as_view()),
]
-------------
Проверяем на странице которая указанна во views.py "product_detail"
-------------
Очевидно, что использовать кэширование можно только с GET HTTP-запросами, т. к.
POST-запрос отправляет данные клиента на сервер, что не совсем подходит под
случай, когда можно использовать кэширование.
Теперь после перехода на кэшируемую страницу в папке cache_files, должны
появиться новые файлы
Теперь, даже если вы попробуете в течение десяти минут (а именно столько
секунд у нас указано в аргументе в декораторе в секундах) изменить товар
(например, напрямую через БД или админ-панель), то пользователь не увидит
изменений. Ему по-прежнему будет показываться старая информация, и так будет,
пока время кэширования не истечёт. Так оно и работает. При этом обратите
внимание, что SQL-запросы в кэшируемой страничке выполняться не будут вообще,
т. к. всё уже хранится в файле. Нагрузка на базу данных снята, что нам и
требовалось.
-------------
Есть ещё способ, который позволяет кэшировать ВЕСЬ САЙТ целиком (т. е. каждую
страницу вообще).
Для этого надо в settings.py добавить в список MIDDLEWARE следующие строки:
settings.py

MIDDLEWARE = [
    ...............
    'allauth.account.middleware.AccountMiddleware',

    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]
И изменить в настройке CACHES:
CACHES = {
    'default': {
        'TIMEOUT': 60,  # добавляем стандартное время ожидания в минуту
                        # (по умолчанию это 5 минут — 300 секунд)
        'BACKEND':
            'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files') # Указываем, куда
        # будем сохранять кэшируемые файлы! Не забываем создать папку
        # cache_files внутри папки с manag8=ъ/e.py!
    }
}
-------------
Обычно этим способом пользуются, если информация, находящаяся на сайте,
практически не меняется или редактируется и обновляется крайне редко.
Например, какие-нибудь интернет-каталоги.
    Кэширование HTML-шаблонов.
Оно используется, если нам надо ограничить запросы в БД или какие-то
вычисления, выполняемые именно в шаблонах. Т. е. не менять всё представление,
а просто сохранить в кэш какие-то элементы странички, шапки, сайдбары и т. д.
Иными словами, сохранять в кэш какие-то отдельные блоки HTML для более
быстрого вызова их в следующий раз.
-------------
Для того, чтобы загрузить кэширование в HTML-шаблон, во-первых, кэширование
уже должно быть настроено у вас в приложении, а во-вторых, должен быть загружен
сам кэш с помощью тега {% load cache %}.
Например, кэширование шапки в шаблонах выглядело бы примерно так:

{% load cache %} <!-- Загружаем кэширование -->
    {% cache 30 header %} <!-- Кэшируем отдельный блок на 30 секунд -->
        {% block header %}
        {% endblock header %}
    {% endcache %}
-------------
Тег кэш имеет следующий синтаксис:

{% cache <количество секунд на которое надо кэшировать> <айди кэширования> %}

Сразу хочется отметить, что не стоит кэшировать блок контента в base.html, в
таком случае это ничем не будет отличаться от кэширования всего сайта целиком,
что уже неприемлемо для нас.
---------------------------------------
Кэширование на низком уровне
----------------------------------------//
Как мы проходили кэширование в Redis?
Для этого и нужен низкоуровневый кэш-апи. Если вы помните Redis, то ничего
принципиально отличающегося.
Специфика работы с низкуровневым кэшем в Django.
    Сделать так, чтобы детали товара кэшировались до тех пор, пока они не
изменятся. Для этого перейдём в sample_app/views.py, чтобы переопределить в
DetailView метод получения объекта.
-------------
simpleapp/views.py

from django.core.cache import cache  # импортируем наш кэш

class ProductDetail(DetailView):
    # Модель всё та же, но мы хотим получить информацию по отдельному товару
    model = Product
    # Используем другой шаблон product.html
    template_name = 'product.html'
    # Название в котором будет выбранный пользователем продукт
    context_object_name = 'product'
    queryset = Product.objects.all()

    def get_object(self, *args, **kwargs):  # переопределяем метод получения
        # объекта, как ни странно
        obj = cache.get(f'product-{self.kwargs["pk"]}', None)  # # кэш очень
        # Похож на словарь, и метод get действует так же. Он забирает значение
        # по ключу, если его нет, то забирает None.
        # Если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)
        return obj
-------------
Если объекта нет в кэше, то мы берём его из БД и кэшируем, а если есть, то
сразу берём из кэша и возвращаем. Но! Давайте узнаем, что же будет происходить
сейчас (не забудьте убрать кэширование из urls.py , иначе получится очень
грязно!).
-------------
Убрал из:
settings.py

    # 'django.middleware.cache.UpdateCacheMiddleware',
    # 'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
Иначе будет происходить кеширование всего сайта.
-----
 # 'TIMEOUT': 60,
-------------
simpleapp/urls.py
Вернул как было
path('<int:pk>', cache_page(60)(ProductDetail.as_view()),
-------------
    Зайдите на кэшируемую страницу и попробуйте через админ-панель что-либо в
ней поменять, а потом обновите страницу.
И тут-то вас ждёт сюрприз! Весь нюанс в том, что теперь ничего не поменяется
вообще… никогда... Ведь мы не установили реакцию на редактирование объекта.
Когда объект меняется его надо удалять из кэша, чтобы ключ сбрасывался и
больше не находился.
-------------
Переопределим метод save в:
simpleapp/models.py

from django.core.cache import cache

class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    quantity = models.IntegerField(
        validators=[MinValueValidator(0,
                                      'Quantity should be >= 0')])
    # Поле которое будет ссылаться на модель категории
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE,
                                 related_name='products')
    # все продукты в категории будут доступны через поле products
    price = models.FloatField(
        validators=[MinValueValidator(0.0,
                                      'Price should be >= 0')])

    def __str__(self):
        return f'{self.category} : {self.name} : {self.description[:20]}'

    # Добавим absolute_urls
    def get_absolute_url(self):
        return f'/products/{self.id}' # добавим абсолютный путь, чтобы после
                            создания нас перебрасывало на страницу с товаром
        # return reverse('product_detail', args=[str(self.id)]) # это было

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы
                                        объект сохранился
        cache.delete(f'product-{self.pk}')   # затем удаляем его из кэша,
                                                чтобы сбросить его
-------------
Вот и всё. Правда, теперь будет тяжело проверить работу самого кэширования,
т. к. в небольших проектах и тем более на локальном сервере нагрузок нет
вообще, и большого прироста мы не почувствуем, но, тем не менее, при
разработке это помогает понять суть самого явления кэширования и научиться в
дальнейшем применять кэширование в боевых проектах, экономя при этом ресурсы
сервера и увеличивая производительность.
---------------------------------------
==============================================================================
D_9                                                                        D_9
==============================================================================
Тестирование кода
Ручное тестирование - делаются напрямую руками разработчика.
Однако, как и многие процессы в разработке, тестирование можно
автоматизировать: написать тесты, которые можно запускать одним нажатием кнопки
или запуском скрипта, и использовать их вместо того, чтобы делать одно и то же
руками.
------------
В теории автоматические тесты делятся на юнит-тесты и функциональные тесты.
• Юнит-тесты — это тесты, проверяющие работу конкретного участка кода
    (функции, класса, модуля).
• Функциональные тесты — это тесты, проверяющие функционал разрабатываемого
    приложения, то есть отвечающие непосредственно на вопрос: «а работает ли моя
программа именно так, как мне надо?».
------------
В зависимости от специфики конкретной программы выделяют также тесты
безопасности, юзабилити (то есть удобства использования) и локализации
(то есть переводов).
---------------------------------------
Юнит тест:
deftest__get_grouped_usser_bills__empty_user_list():
    users = []
    result = get_grouped_bells(users)
    assertresult == {}
из названия теста, и из дальнейшего кода ясно — мы проверяем, работает ли
функция на пустом списке.
-------------
deftest__get_grouped_user_bills__breaks_when_not_user_set():
    user = get_user(id=123)
    post = get_post(id=111)
    users = [user, post]
    try:
        result = get_grouped_bills(users)
        assert False
    except:
        assert True

 из названия теста, и из дальнейшего кода ясно — мы проверяем, работает ли
 функция на списке, в котором есть что-то, кроме пользователе
-------------
TDD (Test-Driven Development — разработка на основе тестов
    Его суть в том, чтобы по возможности писать сначала тесты, а потом уже код,
который они будут тестировать. Таким образом, разработчик, во-первых, сначала
думает об архитектуре кода, а потом уже о том, как именно он его напишет
(порождая таким образом лучше структурированный код), а во-вторых, получает
больше удовольствия от разработки — ведь гораздо приятнее смотреть, как тесты,
которые сначала «падали», постепенно начинают «проходить», а не разрабатывать
огромный кусок кода и только потом выяснять, что он не работает.
    Чтобы подробно разобраться в TDD, рекомендуем прочитать книгу
Роберта Мартина «Чистый код».
-------------
Какие вещи тестировать не нужно.
• Почти никогда не нужно тестировать внешние зависимости — библиотеки и
фреймворки, которые используются в вашем проекте. У них, скорее всего, уже
есть свои тесты, да и не ваша это обязанность — поддерживать чужой продукт
(если, конечно, вы не участвуете в его разработке в рамках open source, но это
уже отдельная история).
• Не нужно тестировать ситуации, в которых ваш код со стопроцентной
вероятностью
использоваться не будет: например, если вы написали функцию для преобразования
даты в строку, и правильность типа передаваемого аргумента обеспечивается вашим
фреймворком или другими инструментами, то не стоит тратить силы на то, чтобы
протестировать ситуацию, когда кто-то передает в вашу функцию что-то, кроме даты.
• Не нужно писать по миллиону тестов на один и тот же случай: в том же примере
с функцией, преобразующей дату в строку, если бы мы решили, что нам всё-таки
нужно проверять в тестах ситуацию с неправильным типом передаваемого аргумента,
то совершенно необязательно было бы писать по тесту на каждый возможный
неправильный тип: достаточно было бы проверить пару очевидных вариантов и
закончить на этом.
-------------
Допустим, мы пишем Telegram-бота. Какие из следующих тестов нам стоит написать?
• Тест на случай, если пользователь должен был отправить картинку,
но отправил файл. Достаточно частая проблема в Telegram.
• Тест на случай, если боту параллельно пишут несколько пользователей
    С большинством ботов такое происходит достаточно часто. Может показаться,
 что это функционал используемой нами библиотеки, и тестировать его не стоит,
 однако наш бот, скорее всего, будет работать с какими-то данными на нашей
 стороне, а это уже наша зона ответственности.
---------------------------------------
Авто проверка кода
    В Python этот стандарт закреплен в документе PEP8.
поговорим о двух наиболее популярных и удобных из этих
инструментов — утилитах Flake8 и PyLint.
Решают одну и ту же задачу — проверку кода на соблюдение стандартов качества
-------------
Flake8 и PyLint

Случай использования	Flake8	            PyLint
Установка	            pip install flake8	pip install pylint
Получить справку	    flake8 --help	    pylint
Проанализировать        flake8 <filename>	pylint <filename>
конкретный файл или
модуль
-------------
А вот вывод этих утилит при анализе файлов/модулей немного отличается.
У каждой из них свои коды ошибок (их полные списки можно найти в документации
каждой из утилит), и, кроме того, PyLint, в отличие от Flake8, даёт числовую
оценку вашему коду после анализа.
-------------
pip install flake8
pip install pylint
-------------
Создадим файл example.py
example.py

import string;

shift = 3
choice = input("would you like to encode or decode?")
word = input("Please enter text")
letters = string.ascii_letters + string.punctuation + string.digits
encoded = ''
if choice == "encode":
    for letter in word:
        if letter == ' ':
            encoded = encoded + ' '
        else:
            x = letters.index(letter) + shift
            encoded = encoded + letters[x]
if choice == "decode":
    for letter in word:
        if letter == ' ':
            encoded = encoded + '  '
        else:
            x = letters.index(letter) - shift
            encoded = encoded + letters[x]
print(encoded)
-------------
И протестируем его с помощью

flake8 example.py
example.py:1:14: E703 statement ends with a semicolon
-------------
(venv) PS C:\Users\feron\Kurss_D\django_d4> pylint example.py
************* Module example
example.py:1:0: W0301: Unnecessary semicolon (unnecessary-semicolon)
example.py:1:0: C0114: Missing module docstring (missing-module-docstring)
example.py:3:0: C0103: Constant name "shift" doesn't conform to UPPER_CASE naming styl
e (invalid-name)
example.py:6:0: C0103: Constant name "letters" doesn't conform to UPPER_CASE naming st
yle (invalid-name)
example.py:7:0: C0103: Constant name "encoded" doesn't conform to UPPER_CASE naming st
example.py:20:12: C0103: Constant name "x" doesn't conform to UPPER_CASE naming style
(invalid-name)
example.py:21:12: C0103: Constant name "encoded" doesn't conform to UPPER_CASE naming
style (invalid-name)

------------------------------------------------------------------
Your code has been rated at 4.21/10 (previous run: 4.21/10, +0.00)
-------------
PyLint нашёл больше проблем, чем Flake8. Даже в рамках PEP8 при настройках по
умолчанию эти утилиты работают по-разному, поэтому код, проверенный одной из
них, необязательно «понравится» другой. Следовательно, очень важно в рамках
проекта, команды и компании использовать одну конкретную утилиту.
-------------
Наконец, обе утилиты можно конфигурировать в соответствии со своими стандартами
-------------
Случай использования	        Flake8	            PyLint
Где можно хранить       В папке пользователя или    В файле pylintrc или
конфигурацию            внутри проекта в файлах     .pylintrc либо в папке проекта,
                        setup.cfg, tox.ini          либо в папке конкретного модуля,
                        или .flake8                 либо в папке пользователя,
		                                            либо в /etc

Формат конфигурации	    INI	                        Свой, типичный для
                                                     rc-файлов
---------------------------------------
Пожалуй, наиболее удобный сценарий использования утилит для проверки кода для
большинства программистов — интеграция со своей IDE.
Большинство популярных IDE автоматически «подхватывают» настройки нужной
утилиты для проекта и используют ее для отображения в графическом интерфейсе
программы ошибок, так что самому разработчику остается только править
найденные ошибки.
---------------------------------------
Документация кода
-------------
ХОРОШИЙ КОД ДОКУМЕНТИРУЕТ САМ СЕБЯ.
---------------------------------------
Пример кода как делать не нужно
-------------
async def process_messages(messages, do_async):
    for message in messages:
        try:
            user_id = message['user']['id']
            user = db_conn.get('user', 'id=={}'.format(user_id))
            user.messages = user.messages + '\n' + message['text']
            user.save()
            if do_async:
                await db_conn.write_async(
                    'message',
                    {'text': message['text'], 'user_id': message['user']['id']}
                )
            else:
                db_conn.write(
                    'message',
                    {'text': message['text'], 'user_id': message['user']['id']}
                )
            return 200, 'OK'
        except DatabaseException as exc:
            return 400, str(exc)
-------------
Это тот-же код только после рефакторинга
-------------
import functools

def catch_db_exceptions(wrapped):
    @functools.wraps(wrapped)
    def wrapper(*args, **kwargs):
        try:
            return wrapped(*args, **kwargs)
        except DatabaseException as exc:
            return 400, str(exc)
    return wrapper

def get_user(user_id):
    return db_conn.get('user', 'id=={}'.format(user_id))

def update_user_messages(user, message):
    user.messages = user.messages + '\n' + message['text']
    user.save()

async def process_message(message, do_async):
    data = {
        'text': message['text'],
        'user_id': message['user']['id']
    }
    if do_async:
        await db_conn.write_async('message', data)
    else:
        db_conn.write('message', data)

@catch_db_exceptions
async def process_messages(messages, do_async):
    for message in messages:
        user = get_user(message['user']['id'])
        update_user_messages(user, message)
        await process_message(message, do_async)
        return 200, 'OK'
---------------------------------------
С одной стороны, кода стало немного больше, с другой — глядя на конкретную
функцию, мы сразу понимаем, что именно она делает и какие функции вызывает:
вместо того, чтобы делить код на участки в голове, мы делаем это
непосредственно в коде. Ситуация улучшается ещё и тем, что созданные нами
атомарные (то есть делающие одну небольшую задачу) функции можно будет легко
переиспользовать в других местах, уменьшая общее количество написанного кода.
Помимо этого, соблюдение PEP8 при написании словаря data позволяет сделать его
более читабельным: мы сразу понимаем, сколько в нём ключей, даже не прочитав
его целиком.
-------------
что нужно сделать, чтобы наш код был понятным?
• Выносить часто используемый функционал в отдельные функции
• Соблюдать стандарты качества кода
---------------------------------------
Самый простой инструмент документирования  — это комментарии.
-------------
Взгляните на пример:
@catch_db_exceptions
async def process_messages(messages, do_async):
    for message in messages:
        user = get_user(message['user']['id'])
        update_user_messages(user, message)
        await process_message(message, do_async)
        # we don't return message text here: just "OK"
        # reasons are described in jira.project.com/browse/KEK-11829
        return 200, 'OK'м
-------------
Программист, написавший этот код, подумал о том, кто будет его читать после
него: он объяснил, что конкретный участок кода выглядит именно так, как он
выглядит, не случайно, и даже дал ссылку на более полное объяснение причин
этого решения. Делать так абсолютно со всем кодом, конечно, не стоит:
комментарии — это инструмент для случая, когда у вашего коллеги могут
возникнуть сомнения в том, правильно ли написан конкретный участок кода.
-------------
Ещё один случай использования комментариев — это работа, оставленная на потом,
или так называемые TODO.
Такие комментарии выглядят следующим образом:
-------------
@catch_db_exceptions
async def process_messages(messages, do_async):
    for message in messages: # FIXME ignore hidden messages
        user = get_user(message['user']['id'])
        update_user_messages(user, message) # TODO use async
        await process_message(message, do_async)
        return 200, 'OK
-------------
Такие комментарии принято оставлять либо себе, либо коллегам — на будущее,
чтобы не забыть сделать что-то важное, но не срочное:

FIXME — для того, чтобы не забыть что-то исправить.
TODO — для того, чтобы не забыть просто что-то сделать.
Многие IDE умеют автоматически подсвечивать такие комментарии.
---------------------------------------
Встроенные в Python документационные строки (docstrings).
    Они используются уже в качестве документации скорее для того, кто будет
пользоваться кодом, нежели для того, кто пишет его вместе с нами. Вы могли
уже видеть докстроки в вашей IDE, наводя мышку на конкретный модуль или
функцию, во всплывающей подсказке.
-------------
для модуля докстрока располагается на первой строчке модуля и заключается в
тройные кавычки. Для функции всё абсолютно аналогично: докстрока в тройных
кавычках пишется на первой строке функции, до того, как будет выполнен
какой-либо код.
Чем лаконичнее докстрока, тем лучше: читатель сумеет быстрее понять суть
происходящего. Поэтому принято по возможности сокращать докстроки до одной
строчки
-------------
Пример:

@catch_db_exceptions
async def process_messages(messages, do_async):
    """Process each message and update them in the user info."""
    for message in messages:
        user = get_user(message['user']['id'])
        update_user_messages(user, message)
        await process_message(message, do_async)
        return 200, 'OK
-------------
Принято писать докстроки, описывая, что делает функция,
в повелительном наклонении
-------------
Иногда важно описать, за что отвечают аргументы функции, или просто дать
читателю больше контекста, и в таком случае докстроки можно разнести на
несколько строк. На строчке с первыми кавычками при этом необходимо оставить
краткую справку о функции:
-------------
@catch_db_exceptions
async def process_messages(messages, do_async):
    """Process each message and update them in the user info.

    You can use this function as a shortcut when you don't care
    about manually specifying parameters for the update and just
    want control over whether or not messages will be processed
    synchronously.

    Parameters
        ----------
        messages : list[Message]
            List of messages
        do_async : bool
            Whether to run the processing asynchronously
    """
    for message in messages:
        user = get_user(message['user']['id'])
        update_user_messages(user, message)
        await process_message(message, do_async)
        return 200, 'OK'
-------------
В такой докстроке есть больше информации о функции, а также описание всех
параметров и их типов. Как именно описывать параметры — вопрос вкусов и
стандартов конкретного проекта/команды/компании, а показанный здесь
формат — лишь один из наиболее популярных.
-------------
Для классов докстроки составляются аналогично: можно писать однострочные, а
можно многострочные, в которых будут описаны методы и переменные класса.
При этом для каждого метода можно написать свою документацию:
-------------
class DatabaseProcess:
    """
    A process interacting with a database

    Attributes
    ----------
    db_name : str
        database name
    timeout : int
        connection timeout (in ms)

    Methods
    -------
    get(entity_name, id=None)
        Gets entity by name and an optional ID.
    """

    db_name = "users"

    def get(self, entity_name, entity_id=None):
        """Gets entity by name and an optional ID.

        If the argument `entity_id` isn't passed in,
        the first entity is returned.

        Parameters
        ----------
        entity_name: str
            The entity name (also known as the table name).
        entity_id : int, optional
            The ID of the entity.

        Raises
        ------
        DatabaseError
            If the database returned an error.
        """

        return db_conn.get(
            table=entity_name,
            filters=(
                {'id': entity_id}
                if entity_id is not None
                else {}
            )
        )
-------------
Последнее, что нужно знать о докстроках — очень важный факт, позволяющий
понять, как именно многие утилиты и IDE превращают их в полезные всплывающие
подсказки или, как Sphinx, создают из них красивую документацию для всего
проекта, которую можно сразу выкладывать на его сайт (да-да, и так можно было):
докстрока для любого задокументированного объекта: модуля, класса, объекта
класса или функции — доступна через специальный атрибут __doc__. Таким
образом, даже работая с кодом из консоли, вы можете быстро получить
документацию к нему.
-------------
Мы можем получить доступ к этим строкам документации,
используя атрибут __doc__
Атрибут __doc__

Подробнее здесь:
https://pythonist.ru/docstrings-dokumentirovanie-koda-v-python/
---------------------------------------
Анотация типов
-------------
в версии Python 3.6 появилась поддержка аннотаций типов (type hints) и
специальный синтаксис для них. С их помощью можно задавать типы данных для
переменных, полей класса, аргументов функций и возвращаемых значений.
Вот пример для всех этих случаев:
-------------
x: int = 5  # аннотация типа переменной

class Counter:
    x: int = 5  # аннотация типа поля класса

    # аннотация типов аргументов
    def __init__(self: Counter, x: int):
        self.x = x

    # аннотация типов аргументов
    # и типа возвращаемого значения
    def count(self: Counter) -> int:
        self.x += 1
        return self.x
-------------
Обратите внимание: все эти аннотации никак не защитят ваш код на этапе
выполнения или компиляции; они предназначены, во-первых, для ваших коллег в
качестве документации, а во-вторых, для статических анализаторов кода
(примерами которых являются уже обсужденные нами Flake8 и PyLint). Таким
образом, вы всё ещё можете пользоваться всеми преимуществами динамической
типизации, при этом сохраняя безопасность типов на этапе написания кода.
-------------
Что делать, если мы хотим ограничить её двумя или тремя типами? Или если мы
хотим сделать её необязательной? Для этих случаев в стандартной библиотеке
Python есть модуль typing, включающий несколько служебных аннотаций типов.
-------------
Аннотация	  Случай использования	              Пример
Callable	  Объект, который можно вызвать     x: Callable[[int],None]
              как функцию                       (x должен принимать на вход
                                                целое число и возвращать None)

Sequence	  Последовательность                x: Sequence[int]
              (например, list)

Mapping       Объект, поддерживающий            x: Mapping[str, str]
	          получение значения по ключу
	          (например,dict)

Any	           Любой тип	                     x: Any

Union	      Любой из перечисленных типов	     x: Union[int, str, float]

Optional	  То же самое, что Union[X, None]	 def foo(arg: Optional[int] =
                                                 None) -> None:

Literal	      Переменная должна быть равна       mode: Literal['r', 'rb', 'w', 'wb']
              одному из перечисленных значений
-------------
Кроме того, вы можете «собирать» свои сложные типы с помощью таких служебных
аннотаций, как Generic, TypeVar, AnyStr и Protocol, однако необходимость это
делать возникает достаточно редко.
Подробнее здесь: typing — Support for type hints — Python 3.12.0 documentation
https://docs.python.org/3/library/typing.html
-------------
• С помощью служебных аннотаций можно задавать сложные типы - все эти
    аннотации лежат в модуле typing.
• Задать переменную как необязательную можно с помощью аннотации
    Optional - это очень удобная служебная аннотация
-------------
В конце концов, главное — чтобы ваш код работал, а коллеги его понимали.
Пренебрегать ли правилами или нет — решать вам.
---------------------------------------
==============================================================================
D_10 Безопасность                                                        D_10
==============================================================================
Веб - безопасность
-------------
Три столпа безопасности
• Конфиденциальность
    Наиболее часто под информационной безопасностью подразумевают именно
конфиденциальность как предоставление доступа к информации, исходя из принципа
минимальной необходимой осведомленности. Иными словами, доступ к разным
«порциям» информации должны получать только те пользователи, которым это
необходимо и, в ту же очередь, которые имеют права на получение этой информации.
Самый банальный пример — личные данные человека (паспортные данные, банковская
информация). Доступ к ним должен иметь сам владелец данных, а также сервисы и
службы, имеющие на это право (по природе информации или по разрешению самого
владельца прав).
• Целостность
    Второй аспект информационной безопасности касается целостности данных.
Действительно, данные где-то хранятся, как-то обрабатываются и куда-то
передаются. На всех этих этапах могут происходить искажения в виде потери части
информации, появления «шумовой» информации, а также невалидных данных.
Естественно, что такое может происходить и непреднамеренно в силу объективных
обстоятельств, но стоит также понимать, что искажения информации могут
происходить и преднамеренно в виде компьютерных вирусов и других методов
нарушения безопасности. Также возможны и случайные нарушения целостности в силу
неосторожности обращения с данными. Вне зависимости от причин обеспечение
целостности данных подразумевает меры контроля над изменениями информации и
наличие методов восстановления в случае нарушения этой самой целостности.
• Доступность
    И, наконец, третий аспект — доступность. Под этим термином подразумевается
обеспечение возможности получения доступа к системам и информации по требованию.
Иными словами, если существует информация и пользователь, обладающий достаточным
уровнем доступа, то он должен получать его (доступ) беспрепятственно. В таком
случае пользователь может получить одно или несколько прав: на чтение, изменение,
хранение, копирование, удаление информации и др.
-------------
Протокол передачи гипертекста
-------------
• HTTP (Hypertext Transfer Protocol) определяет правила передачи данных в
интернете. Согласно этому протоколу данные передаются в чистом,
незашифрованном виде.
• HTTPS (Hypertext Transfer Protocol Secure) — защищенный протокол передачи
гипертекста. Он не является отдельным протоколом, а скорее расширением
протокола HTTP, который помимо всех существующих правил, обеспечивает
шифрование данных при передаче их через Интернет.
    На текущий момент количество сайтов, работающих по HTTPS превзошло количество
сайтов с HTTP, поэтому специалисты по информационной безопасности настаивают
на использовании именно безопасного протокола. Этому способствует также то,
что популярные браузеры и поисковые системы поощряют сайты, использующие HTTPS.
Например, Google Chrome уведомит пользователя, что он переходит на небезопасный
сайт, если он работает по HTTP, а поиск в Google поднимет сайт при ранжировании,
если используется безопасный протокол, относительно того же сайта с обычным HTTP.
    Для полной реалистичности картины стоит учитывать, что несколько повышается
время загрузки сайта в связи с необходимостью шифрования и дешифрования.
---------------------------------------
SSL и TSL
-------------
• SSL — Secure Sockets Layer;
• TLS — Transport Level Security.
Сами по себе SSL/TLS — это протоколы шифрования, основанные на использовании
цифровых сертификатов. Это наборы данных, подтверждающие подлинность.
Эти сертификаты выдают центры сертификации.
Он делится на две фазы:
1. Фаза «рукопожатия».
2. Фаза самой передачи данных.
-------------
В фазе «рукопожатия» сервер и клиент обмениваются разными данными, чтобы
удостовериться в подлинности друг друга:
• Клиент отправляет запрос серверу на создание безопасного подключения, а также
предоставляет список доступных клиенту алгоритмов шифрования.
• Сервер в свою очередь сверяет этот список со своим списком алгоритмов
шифрования и сообщает клиенту, какой лучше использовать.
• Также он отправляет свой цифровой сертификат и открытый ключ сервера.
• В этот же момент сервер может запросить цифровой сертификат у клиента,
но это необязательно.
• Клиент на этом этапе также может проверить действительность цифрового
сертификата, сделав запрос в центр сертификации.
• Последним шагом должен сформироваться сеансовый ключ защищенного
соединения: клиент генерирует последовательность, шифрует ее открытым ключом
сервера и посылает ее.
---------------------------------------
Same origin policy (SOP)
Правило ограничения домена или политика одинакового источника. Основное
понятие, фигурирующее в этой концепции, — это источник.
    Источником называют комбинацию домена, порта и протокола.
-------------
Например, у нас есть сайт: http://www.example.com/index.html.
Он работает по протоколу HTTP, его домен — www.example.com, и он работает по
порту 80 (по умолчанию он не указывается). Все страницы с этой же комбинацией
относятся к данному источнику: http://www.example.com:80/index.html (явное
указание порта), http://www.example.com/dir/page.html (другая страница в этом
же источнике).
Однако, если изменить хотя бы одну из составляющих,
то это уже будет другой источник:
• https://www.example.com/index.html (изменился протокол);
• http://sub.example.com/index.html (изменился домен);
• http://www.example.com:81/index.html (изменился порт).
Современные сайты используют большое количество контента, являющегося не
просто статическим. Например, сценарии Javascript. И вообще говоря, если у
мошенника есть возможность добавить свой скрипт на ваш сайт, то он перестает
быть безопасным. Благодаря этому вредоносному скрипту может нарушиться один
(или даже все!) столпы безопасности.
Политика одинакового источника регламентирует, что на вашем сайте будут
использоваться только те документы (скрипты, например), которые находятся в том
же самом источнике. Таким образом, даже если мошенники захотят внедрить
вредоносный код на сайт, то он будет сразу же заблокирован, потому что его
источник отличается от источника основного контента!
---------------------------------------
Распространенные угрозы

Классификация существующих угроз:
• Аутентификация
• Авторизация
• Атаки на клиентов (clien-side attacks)
• Выполнение кода (code execution)
• Разглашение информации
• Логические атаки

Все угрозы, представленные в этих группах, нарушают как минимум один принцип
безопасности (конфиденциальность, целостность, доступность). Безответственное
отношение к потенциальным угрозам может привести к серьезным последствиям.
Конечно, здесь вновь стоит напомнить, что даже учет всех этих угроз и
обеспечение защиты от них не дает 100% гарантии. Однако это необходимо делать
для предотвращения преобладающей части попыток нарушения безопасности.
-------------
И действительно, все атаки можно разделить еще на две группы (по другому признаку):
1. Целевые
2. Нецелевые

    В первом случае попытки нарушения безопасности ориентируются на конкретный сайт
или группу схожих сайтов (например, сайтов компании одной отрасли).
    Второй тип атак действует по принципу «массового обстрела». Этот вид атак
запускается на огромное множество сайтов сразу, и ваш может просто попасть
«под раздачу». Анализ угроз вашему сайту и внедрение методов защиты направлено
в основном на нецелевые атаки. Прекрасно стоит понимать, что если целью хакеров
является именно ваш сайт, то он будет скрупулезно искать бреши в защите и при
должном количестве времени и ресурсов сможет что-то найти. От такого вида атак
не защищены на 100% даже самые защищенные сайты.
---------------------------------------
Аутентификация
-------------
    Этот тип атак связан с процессами идентификации и аутентификации пользователей.
С одной стороны, успешность такого рода атак может быть связана с недостаточной
ответственностью самого пользователя (слабые пароли, простые способы
аутентификации и т.д.), с другой — со слабостями самой системы.
-------------
Основные атаки, совершаемые на веб-приложени:
1. Подбор пароля (Brute Force, также в русскоязычной среде называемый брутфорс).
Очень простой алгоритм перебора значений для угадывания паролей, номеров
кредитных карт и данных, которые их защищают (CVV код, например) и др.
2. Недостаточная аутентификация.
Этот вид угроз направлен уже не на пользователя, а именно на сервер. Ранее мы
обсуждали, что существуют различные степени аутентификации — от однофакторной
аутентификации только по паролю до использования более уникальных факторов и
даже двухфакторной аутентификации. И естественно, чем проще организован сам
процесс, тем легче мошенникам будет совершить атаку.
3. Небезопасное восстановление паролей.
Это, пожалуй, ахиллесова пята любой системы паролей. Стоит понимать, что
пользователи всегда будут забывать пароли. И в связи с этим необходим механизм
их восстановления. Наличие такого механизма открывает возможности атакующим для
несанкционированной модификации аутентификационных данных.
---------------------------------------
Авторизация
-------------
Механизм авторизации перераспределяет права доступа для получения к разным
частям веб-приложения и данным. И в целом, можно сказать, что эти атаки
направлены на повышение привилегий прав при авторизации.
-------------
Наиболее частые векторы атак:
1. Предсказуемое значение идентификатора сессии.
Вспомните, что сервер и клиент обмениваются данными, подтверждая подлинность
аутентификационных данных с помощью механизма сессий. Если идентификатор сессии
легко получить, то это дает возможность мошенникам использовать для входа в
сессии других пользователей с, возможно, более высоким уровнем прав вплоть до
администраторских.
2. Недостаточная авторизация.
Здесь подразумевается брешь в самой системе, когда не предусмотрено достаточно
строгое распознавание прав доступа к разным компонентам системы.
3. Отсутствие таймаута сессии.
Чем выше таймаут сессии (время, по истечении которого данные сессии затираются),
тем больше шансов перехватить аутентификационные данные, которые хранятся в ней.
В сервисах, где требуется наиболее высокий уровень безопасности, сессии длятся
очень короткие периоды.
4. Фиксации сессии.
Данный тип атак направлен не столь на предсказание идентификатора сессии,
а на его установку собственным значением.
---------------------------------------
Атаки на клиентов
-------------
Пользователь доверчив — истина, которую используют мошенники для атак на самих
клиентов. Если вы зашли на сайт и, более того, пользуетесь им какое-то время,
то вы не ожидаете, что с этого сайта придут проблемы. И этим пользуются
мошенники. Данный вид атак направлен не на сервер, а на клиентов сервера.
-------------
Основные виды атак:
1. Подмена контента (Content spoofing).
    В случае этой атаки мошенник может генерировать страницы, максимально похожие
на оригинальный сайт. И, например, включить формы с конфиденциальными данными
(пароли, банковские данные и т. д.). В связи с тем, что визуально они могут
быть практически не отличимыми, пользователь доверяет свои данные и со спокойной
душой вводит их, а мошенник радостно их захватывает.
2. Межсайтовое исполнение сценариев (Cross-site Scripting, XSS).
    Мошенник также может внедрить, например, Javascript-сценарий в браузер
пользователя. Появление одного такого достаточно простого сценария может
привести к снятию защит от других, более серьезных атак.
3.  Перехват кликов (clickjacking).
    Этот механизм атак основан на включении скрытых элементов, которые отлавливают
поведение указателя и используют его для своих целей.
4. Расщепление HTTP-запроса.
    Сервер и клиент общаются с помощью HTTP-запросов и сам запрос также может
подвергаться атакам. Действительно, есть возможность модифицировать запрос
(или ответ) в целях, который угоден мошенникам.
---------------------------------------
Выполнение кода
-------------
Клиент постоянно отсылает какие-то данные серверу. В эти данные может быть
«вшит» исполняемый код, и это также одна из брешей защиты.
-------------
Основные атаки:
1. Переполнение буфера (buffer overload).
    Используется для перезаписи данных в памяти системы
2. Функции форматирования строк.
    Путь исполнения запроса на сервере может быть модифицирован методом перезаписи
областей памяти с помощью функций форматирования символьных переменных.
3. Внедрение кода.
    Эта целая группа атак, которая направлена на добавление исполняемого кода в
запросы к базе данных (SQL injection) или, например, добавление команд
операционной системы (OS injection). В зависимости от используемого языка, как
правило интерпретируемого, можно получить доступ к тем или иным компонентам и
тем самым модифицировать ход исполнения запросов на сервере. Например,
веб-приложения на Python/Django могут быть подвержены Python Injection, когда
в запросе к серверу передается текст, который при обработке интерпретатором
воспринимается не просто как текст, а как код, который также будет исполнен.
---------------------------------------
Разглашение информации
-------------
Атаки данного класса служат скорее «разведкой», чем нарушением информации.
Цель таких атак — узнать как можно больше о системе для проведения последующих
атак уже с более конкретными целями.
-------------
К ним относят:
1. Индексирование директорий.
    Эта разведка направлена на получение информации о каталогах и файлах, которые
хранятся на сервере. Ведь действительно на сервере может храниться информация
недоступная при навигации по сайту, и атаки направлены на поиск именно такой
информации.
2. Идентификация приложений.
    Этот вид атак направлен на выяснение подробной информации о сервере или клиенте.
Речь идет об их операционной системе, компонентах, промежуточных сервисах и др.
3.  Утечка информации.
    В этом случае не мошенник разведует слабые места, а сам сайт может их предложить.
Например, если в Django включен флаг Debug=True в настройках проекта, то при
появлении ошибки можно увидеть слишком много информации, которая может
использоваться мошенниками.
4. Предсказуемое расположение ресурсов.
    Традиции создания веб-приложений имеют обратную сторону медали — стандартные
способы организации структуры сайтов и взаимодействия с другими компонентами
приводит к предсказуемому поведению, а значит облегченному доступу к ним у мошенников.
---------------------------------------
Логические атаки
-------------
Данный тип атак заточен на слабые места логики самого веб-приложения.
Сервер ожидает от пользователя какие-то действия, по результатам которых должен
выполнить логическую цепочку действий и вернуть их результат клиенту, вновь
ожидая от него действий. Нарушение этих цепочек взаимодействия может привести
к катастрофичным последствиям.
-------------
Наиболее известные виды атак:
1. Отказ в обслуживании (Denial of Service).
    Более известная как DoS-атака или DDoS-атака. Дополнительная буква D означает
distributed, т. е. распределенная. Этот тип атак направлен на ограничение
доступности веб-приложения. Если говорить простым языком,
цель такой атаки — «положить» сервер. В новостях регулярно появляются такого
рода события. В результате политических, экономических, социальных и других
событий группы хакеров (наиболее известная Anonimous) перенагружают серверы
сайтов разных организаций, компаний, государственные сайты и т. д.
2. Недостаточное противодействие автоматизации.
    Естественно полагать, что сервер требует от клиента ручного взаимодействия с
ним, однако постоянно появляются различные «боты», автоматизирующие эти процессы
вопреки желаниям сервера.
3. Недостаточная проверка процесса.
    Уязвимость, которая появляется вследствие недостаточности проверки
последовательности выполнения операций приложения.
-------------
Данный список, подготовленный при помощи материалов WASC,
---------------------------------------
Методы защиты
-------------
К общим рекомендациям в защите веб-приложения стоит сказать, пожалуй, одну из
самых важных вещей — всегда устанавливайте последние обновления безопасности
для операционных систем и компонентов, которые используются в вашем
веб-приложении. Иногда это может быть критически важно.
---------------------------------------
CORS
-------------
Для обеспечения безопасности веб-приложения работают по принципу
Same origin policy (SOP). Однако, как мы и указали, не всегда в одном
веб-приложении должны использоваться только его ресурсы. Полностью открыть
доступ (ко всем источникам) было бы небезопасно. В связи с этим была
реализована технология ослабления правила одного источника, которая получила
название Cross-Origin Resource Sharing (CORS).
-------------
Допустим у нас есть два ресурса:
http://www.client.net и http://www.server.com.
-------------
Клиент, пользуясь первым ресурсом, по необходимости захотел получить доступ
ко второму ресурсу. Политика SOP такое действие бы запретила, но при
использовании CORS такое возможно, и вот как это происходит:
1. Клиенсткий ресурс отправляет запрос на второй — http://www.server.com.
2. Сервер получает запрос вида:
    GET / HTTP/1.1
    Accept: application/json, text/plain, */*
    Origin: http://www.client.net
   Здесь можно увидеть, что Origin совпадает с тем источником, с которого мы
   отправляем запрос. Сервер в свою очередь отправляет ответ, в котором можно
   найти строку: Access-Control-Allow-Origin: http://www.client.net
3. Эта строка (со стороны запрашиваемого ресурса!) указывает, что данный
    источник (клиентский) может использовать данный ресурс. Однако другому ресурсу,
например, http://www.client.org, сервер не даст такую возможность, потому что
он не указан в списке заголовка Access-Control-Allow-Origin. Можно вместо
указания конкретного источника поставить *, и тогда любой ресурс сможет
получить доступ к текущему. Однако стоит понимать, что это также небезопасно,
но может использоваться для полностью открытых API.
-------------
Иными словами, технология CORS ориентирована на то, чтобы дать возможность
предоставить доступ к определенному ресурсу только тем источникам, которые
указаны в заголовке.
---------------------------------------
CSP
-------------
В чем-то схожая технология, но являющаяся полной противоположностью и, скорее,
дополнением к CORS — это технология Content Security Policy (CSP). Это
дополнительный уровень безопасности, который в основном направлен на защиту от
межсайтового скриптинга (XSS) и Code injection разных видов.
    Если CORS ограничивает список тех, кто может получать доступ к ресурсам,
то цель CSP ограничить список ресурсов, откуда может загружаться контент.
Банальный пример — ограничить список источников, откуда могут загружаться
изображения для страницы.
-------------
Лирическое отступление про изображения.
Они кажутся совсем безобидными — ведь это просто набор пикселей, скажете вы!
Однако атаки типа «внедрение кода» могут совершаться именно через передачу
файлов изображений, встраивая код в файл с изображением. Не нужно недооценивать
мошенников. Ведь скрипты можно внедрить, где угодно.
-------------
Политика CSP описывается с помощью HTTP-заголовка и нескольких директив,
таких как:
• default-src,
• img-src,
• media-src,
• script-src,
-------------
Каждая из директив позволяет ограничивать определенный контент с ресурсов,
которые указаны после директивы. Доступ можно предоставлять как целым доменам,
так и поддоменам, уточнять протоколы их работы или указывать конкретные страницы.
Подробнее здесь:
https://developer.mozilla.org/ru/docs/Web/HTTP/CSP
-------------
Таким образом эта политика реализует принцип
«брать только от доверенных источников»,
а CORS дополняет ее принципом «предоставлять только доверенным источникам».
---------------------------------------
Аутентификация и авторизация
---------------------------------------
Для защиты от атак в областях аутентификации и авторизации вопрос сводится не
столь к применению конкретных технологий, а к правильному подходу реализации
этих процессов.
Самое главное на что стоит обратить внимание — это пароли.
Здесь можно дать лишь несколько советов по обеспечению безопасности:
1. На сервере пароли всегда должны храниться в зашифрованном виде. Никогда и
    ни в коем случае не храните и не отправляйте пароли в незащищенном виде.
2. Требуйте от пользователей использование надежных паролей. Установите
    минимальное количество символов, обязывайте использовать и цифры, и буквы,
и специальные символы (знаки препинания, подчеркивания и т. д.).
Дополнительно можно осуществлять проверку на частоту использования пароля по
словарю и хотя бы предупреждать об этом пользователя.
3. Используйте двухэтапную однофакторную аутентификацию или даже двухфакторную
    аутентификацию. Да, это несколько усложняет процесс как разработки, так
регистрации и входа для пользователей, но поверьте — лучше вложиться в защиту,
чем вкладываться в последствия пробоев в защите.
4.  При неверном вводе пароля в течение нескольких раз предлагайте вводить
    капчу (CAPTCHA) или же создайте таймаут между неудачными попытками входа.
Например, при входе в Google-аккаунт можно проследить, что после 5 неудачных
попыток двухфакторной аутентификации в аккаунт невозможно войти в течение суток.
Этот подход повысит защиту от автоматических попыток входа с помощью брутфорса
и различных ботов.
5. Реализуйте надежный механизм восстановления пароля, который может проверять
    другие идентификационные данные помимо тех, что вводятся пользователем при
логировании. Например, дополнительная почта, номер телефона, если вход по
почте и наоборот не по почте, если вход по телефону и т. д.
6.  Настраивайте срок действия сессий! Чем длительнее сессия, тем проще
    получить ее данные (идентификатор и аутентификационные данные, которые могут
находиться в ней).
7. Внимательно следите за предоставлением прав группам пользователей к
    определенным частям контента. Одна лишь неточность может привести к
несанкционированным действиям с данными.
---------------------------------------
Специализированные средства защиты
---------------------------------------
специализированные средства защиты — Web Application Firewall.
-------------
Их принцип работы заключается в мониторинге HTTP-трафика от пользователей до
веб-приложения. Это может быть реализовано двумя способами — весь трафик будет
сначала попадать в фаервол и из него идти в веб-приложение, либо в фаервол
будет попадать копия трафика. В первом случае атаки могут быть заблокированы
«на месте», во втором случае — в результате мониторинга могут приходить
оповещения об атаках.
-------------
WAF имеет огромное количество инструментов анализа и предотвращения угроз от
ручной настройки правил до интеллектуального анализа трафика. В совокупности
они позволяют вывести уровень безопасности приложения на новый уровень.
-------------
Отдельно стоит отметить такие средства, как балансировщики нагрузки, которые
позволяют перераспределять нагрузку на сервер и его компоненты, что позволяет
повысить отказоустойчивость системы. Например, эти средства могут помочь в
борьбе с переполнением буфера.
-------------
И отдельно стоят средства, направленные на борьбу с DDoS-атаками.
---------------------------------------
Защита от угроз в Django
---------------------------------------
Межсайтовый скриптинг (XSS)
Атаки XSS направлены на внедрение вредоносных скриптов на страницу сайта.
Такая атака может быть совершена, например, путем ввода скрипта в форму сайта.
Допустим, что в приложении есть форма, в которую пользователь должен ввести
какой-то текст. Вместо обычного текста мы можем ввести Javascript-код, который
выводит уведомление (в качестве примера).
Код вызова этого уведомления:
<script> alert('Evil script');</script>

Без использования защиты от XSS-атак после нажатия кнопки «Отправить»,
пользователь бы получил уведомление (новое окно внутри страницы) с подписью
Evil script. Атака совершена. Однако Django умен и он знает, что угловые
скобки <,> — это специальные символы HTML-тегов. Вместо прямого использования,
он заменяет их на код символа. Скобка «>» заменится на «%gt;».
---------------------------------------
Межсайтовая подделка запросов (CSRF)
-------------
При создании форм мы обязательно должны были включать
некоторый csrf_token в шаблон формы.
    Один из способов атаки — передача HTML-страницы с заранее подготовленной
 формой.
Если эту страницу откроет залогиненный пользователь, то при открытии этой
страницы тут же отправится форма на сервер со всеми введенными данными.
Опасно! Ведь можно внедрить в базу данных абсолютно любые данные.
    Для защиты от таких действий служит CSRF Token. Это уникальная строка,
состоящая из букв и цифр, которая передается от сервера к пользователю и
возвращается обратно серверу после заполнения формы. Если сервер получил данные
формы без этого токена, то он отклоняет ее. Конечно и этот уникальный токен
можно получить, но тогда снижается характер массовости такой атаки. Защита от
CSRF-атак включена в Django по умолчанию. Разработчику следует только
использовать в шаблонах тег:

{% csrf_token %}
---------------------------------------
Безопасный протокол передачи (HTTPS)
-------------
Django позволяет использовать HTTPS и предоставляет следующие методы защиты:

1. SECURE_PROXY_SSL_HEADER
        Используется для проверки, что подключение всегда безопасное, даже
        если данные поступают из небезопасного (HTTP) прокси.
2. SECURE_SSL_REDIRECT
        Используется для перенаправления всех запросов с HTTP на HTTPS.
        Это обсуждалось ранее.
3. SESSION_COOKIE_SECURE/CSRF_COOKIE_SECURE
        Флаги, которые жестко устанавливают передачу данных cookie только
        через протокол HTTPS.
4. ALLOWED_HOSTS
        Список доверенных хостов.
---------------------------------------
Другие методы защиты
-------------
Если не вдаваться в технические подробности реализации методов защиты, то
можно лишь сказать, что фреймворк позволяет усилить защиту
для следующих атак:

1. SQL injection
    Защита от такого вида атак достигается использованием Django ORM. Они, можно
сказать, экранируют прямое написание SQL-запросов от пользователя. Конечно,
существуют способы «ручного» написания запросов, и с ними нужно быть
осторожными, но это более редкая возможность.
2. Clickjaking
Для обеспечения защиты от перехвата кликов, Django использует промежуточное
программное обеспечение (middleware), который поддерживается браузерами.
Его цель — запрет отображения скрытых элементов на страницах, которые как раз
и служит для кликджекинга.
3. Подделка контента и загрузка небезопасного контента.
В Django реализована проверка загружаемого контента (например, изображений) с
помощью встроенных классов (FileField, ImageField). Также есть возможности для
ограничения размеров загрузок, что также позволяет защититься от DoS-атак.
-------------
Django содержит один полезный инструмент для проверки безопасности вашего
приложения на основные угрозы.
Из корня приложения можно запустить команду:

python3 manage.py check --deploy
-------------
Результатом ее выполнения является анализ приложения на наличие ошибок, угроз
безопасности и др. Использование этой команды может быть также полезным при
рассмотрении вашего приложения с точки зрения безопасности.
---------------------------------------
pip freeze
Команда генерирует список всех установленных пакетов с их версиями для того
чтобы их установить
amqp==5.1.1
APScheduler==3.10.4
asgiref==3.7.2
astroid==3.0.1
async-timeout==4.0.3
billiard==4.1.0
celery==5.3.4
certifi==2023.7.22
cffi==1.16.0
charset-normalizer==3.3.0
click==8.1.7
click-didyoumean==0.3.0
click-plugins==1.1.1
click-repl==0.3.0
colorama==0.4.6
cryptography==41.0.4
defusedxml==0.7.1
dill==0.3.7
Django==4.2.6
django-allauth==0.57.0
django-apscheduler==0.6.2
django-filter==23.3
flake8==6.1.0
idna==3.4
isort==5.12.0
kombu==5.3.2
mccabe==0.7.0
oauthlib==3.2.2
platformdirs==3.11.0
prompt-toolkit==3.0.39
pycodestyle==2.11.1
pycparser==2.21
pyflakes==3.1.0
PyJWT==2.8.0
pylint==3.0.2
python-dateutil==2.8.2
python3-openid==3.2.0
pytz==2023.3.post1
redis==4.6.0
requests==2.31.0
requests-oauthlib==1.3.1
six==1.16.0
sqlparse==0.4.4
tomli==2.0.1
tomlkit==0.12.1
typing_extensions==4.8.0
tzdata==2023.3
tzlocal==5.1
urllib3==2.0.7
value==0.1.0
vine==5.0.0
wcwidth==0.2.8
-------------
Создаёт файл со списком пакетов для последующей установки
pip freeze > requirments.txt
Устанавливаем все пакеты из файла
pip install -r requirments.txt
---------------------------------------
==============================================================================
D_11 Управляющие команды и настройка панели администратора ШАБЛОНЫ       D_11
==============================================================================
Управляющие команды Django — это команды, которые позволяют выполнять работу
    с вашим проектом, не меняя при этом его исходного кода, например, команда
как-либо изменить базу данных, создать нового пользователя и т. д.
django-admin startproject <имя проекта>
Подрробнее здесь: https://docs.djangoproject.com/en/3.1/ref/django-admin/
-------------
Обычно мы привыкли видеть что-то в виде: manage.py <команда> <параметры>, а в
итоге видим следующее: django-admin <команда> <параметры>. Сразу нужно
отметить, что разницы никакой здесь нет. Однако для того, чтобы использовать
команды с помощью django-admin вам надо перейти в виртуальную среду вашего
проекта (venv/bin/activate — Linux, Macos; venv\scripts\activate — Windows) и
указать в переменную среды DJANGO_SETTINGS_MODULE путь к файлу settings.py
вашего проекта.
Например, это можно сделать так:

export DJANGO_SETTINGS_MODULE=<путь к файлу настроек>.settings — для Linux
set DJANGO_SETTINGS_MODULE=<путь к файлу настроек>.settings — для Windows.
-------------
Давайте посмотрим на уже знакомую нам команду создания нового приложения
внутри проекта, мы можем кастомизировать создание нашего приложения.

Например, помимо основного параметра — имя приложения, мы можем ещё указать
дополнительные аргументы этой команде. Мы можем создать приложение в другой
папке или же распаковать шаблон приложения (об этом чуть позже) прямо в папку
с проектом, просто введя вместо пути точку — «.», например:

python manage.py startapp myapp .
Команда создаст приложение прямо в той же папке, что и manage.py, но можно
создать приложение, например, и в другой папке. Или же можно помещать ваши
приложения в отдельно заготовленную для этого папку, например, так:

django-admin startapp app apps/app
Создаём приложение app в дериктории apps
---------------------------------------
Одной из фишек базовых команд, является возможность создавать проекты или
приложения по шаблону.
    При создании проекта помимо пути можно также указать дополнительный
аргумент --template и указать шаблон для панели, на основе которого надо
будет создать проект.
Но для начала надо подготовить саму болванку, т. е. шаблон. Для этого надо
создать новый проект и везде поменять название проекта на {{ project_name }}.
-------------
Например, файл manage.py выглядел бы так:
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{project_name}}.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
-------------
settings.py
"""
Django settings for {{project_name}} project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '{{secret_key}}' # здесь ещё надо поменять секретный ключ, чтобы в целях безопасности он генерировался всегда по новой

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '{{project_name}}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = '{{project_name}}.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = 'https://lms-cdn.skillfactory.ru/static/edx-theme/'
-------------
asgi.py
"""
ASGI config for project_name project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{project_name}}.settings')

application = get_asgi_application()
-------------
wsgi.py
"""
WSGI config for project_name project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{project_name}}.settings')

application = get_wsgi_application()
-------------
После этого можно создавать новый проект по имеющемуся шаблону.

django-admin startproject --template=project_name tutorial
-------------
И теперь у вас должно появится приложение по шаблону вашего проекта. Туда уже
может быть встроен какой-либо функционал или же, наоборот, можно превратить
ваш готовый проект в шаблон, выполнив те же действия.
Можно даже перейти в папку tutorial с проектом и попробовать запустить его:

python tutorial/manage.py runserver
---------------------------------------
Подобная процедура также выполнима и с приложениями.
---------------------------------------
Также немаловажной командой при развертывании ваших проектов может быть
команда по сбору статических файлов/
    Она нужна только в том случае, когда ваш сайт по какой-то причине потерял
все статические файлы, такие как стили, js-скрипты и т. д.
Просто введите в корне проекта python manage.py collectstatic.
Это должно помочь.
---------------------------------------
Следующая немаловажная команда — создать суперпользователя.

python manage.py createsuperuser
-------------
К слову, если вы вдруг забыли пароль от админа — вовсе не обязательно создавать нового, достаточно сбросить пароль:
python manage.py changepassword <имя пользователя>
-------------------Раббота с БД--------------------
Команды для работы с базами данных
• python manage.py makemigrations [<имя приложения>] — создание миграций
    (обратите внимание, что имя приложения — параметр необязательный, если его
указать, то создаются только миграции для конкретного приложения)
• python manage.py migrate — применить созданные миграции, т.е. внести
    изменения уже именно в саму базу данных
(создать новые или редактировать старые модели).
• python manage.py showmigrations — показать все изменения вносимые в
    базу данных. Довольно удобная штука для того, чтобы можно было отслеживать
    изменения моделей.
-------------
Можно выгрузить данные из вашей базы данных в каком-либо формате.
Давайте попробуем выгрузить все записи из нашей БД в JSON-файл:
---------Работа с БД если в БД есть кирилица--------
Создаёт копию БД в формате json и xml

python -Xutf8 manage.py dumpdata --format=json --output mydata.json
python -Xutf8 manage.py dumpdata --format=xml --output mydata.xml

Загружаем в БД

python manage.py loaddata mydata.json
python manage.py loaddata mydata.xml
python manage.py dumpdata --format=json > mydata.json
-------------
Если при загрузке в БД выходит ошибка нужно закомментировать метод post-save
и повторить
Подробнее здесь:
https://stackoverflow.com/questions/13668728/failing-fixture-load-doesnotexist-matching-query-does-not-exist/13668774#13668774

signals.py
Закоментировал всё
models.py  закомментировал этот метод

   def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'product-{self.pk}')
после этого
python manage.py loaddata mydata.json
ответ
Installed 269 object(s) from 1 fixture(s)
т.е. всё хорошо
-------------
В нём обычному человеку мало что удастся понять, т. к. он структурирован
специально под задачи Django, чтобы эти данные можно было в любой момент
загрузить обратно в базу. И перед тем, как мы этим займёмся, давайте попробуем
выгрузить наши данные, но уже в другом формате:

python manage.py dumpdata --format=xml > mydata.xml
-------------
Так, ну и теперь попробуем удалить данные через админ-панель и снова загрузить
их, но уже через команду loaddata:

python manage.py loaddata mydata.json
-------------
В итоге у нас должно появится следующее сообщение в консоли:

Installed 3 object(s) from 1 fixture(s)

Это говорит о том, что данные снова загрузились успешно! (Постарайтесь,
чтобы в ваших объектах не было полей с русскими буквами, иначе можно жёстко
застрять с кодировкой).
---------------------------------------
Последние две команды могут служить для самых разных целей, но, как правило,
в большинстве случаев, они используются для создания тестовых данных.
Например, данных для базы данных тестового сервера или же фикстур для тестов
(тесты мы затронем немножко попозже, но это тоже довольно интересная вещь).
Также не обязательно выгружать целиком данные из всего проекта, можно
выгрузить данные из какого-то одного приложения, для этого достаточно
добавить аргумент с названием приложения:

python manage.py dumpdata --format=xml sample_app > sampledata.xml
-------------
Параметр --database может указывать на базу данных (названия берутся из
настроек), из которой будут выгружаться или в которую будут загружаться
данные, на случай если у вас их несколько.
Ну и команда экстерминатус — полная очистка базы данных, т. е. удаление всех
данных из таблиц в ней.

python manage.py flush

Если у вас несколько баз данных, то можно указать всё тот же параметр
--database и очистить какую-то конкретную БД.
---------------------------------------
Написание собственных команд
    Подробнее здесь:
https://docs.djangoproject.com/en/3.1/howto/custom-management-commands/
-------------
Для того чтобы создать собственную команду надо выбрать приложение, с которым
она будет логически связана, и создать в его папке следующую структуру,
например так:

sample_app/management/commands/<имя вашей команды>.py
-------------
Далее надо создать класс самой команды. Определенные методы этого класса будут
отвечать за то или иное поведение во время выполнения вашей команды.

Пример создания класса-команды:
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Подсказка вашей команды' # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    missing_args_message = 'Недостаточно аргументов'
    requires_migrations_checks = True # напоминать ли о миграциях. Если тру — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('argument', nargs='+', type=int)

    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполняется при вызове вашей команды
        self.stdout.write(str(options['argument']))
-------------
Запускается она также, как и любая другая команда,название вашего файла и
есть название самой команды!
python manage.py runmycommand
-----Пример--------
Создаём дерикторию с файлом в дериктории приложения там где находится
models.py
simpleapp/management/commands/nullfyquantity.py

from django.core.management.base import BaseCommand, CommandError
from simpleapp.models import Product

class Command(BaseCommand):
    help = "Обнуляет количество всех товаров"

    def handle(self, *args, **options):
        for product in Product.objects.all():
            product.quantity = 10
            product.save()

            self.stdout.write(self.style.SUCCESS(
                'Successfully nulled product "%s"' % str(product)))
------
self.style.SUCCESS # натпись зелёная
self.style.ERROR   # красная
-------------Запускаем----
python manage.py nullfyquantity

python manage.py nullfyquantity --help
 выводит то что написанно в переменной help. Таким образом можно писать
 документацию к командам.
-------------Команда удаляет все товары------
from django.core.management.base import BaseCommand, CommandError
from simpleapp.models import Product


class Command(BaseCommand):
    help = 'Подсказка вашей команды' # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True # напоминать ли о миграциях. Если тру — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполнется при вызове вашей команды
        self.stdout.readable()
        self.stdout.write('Do you really want to delete all products? yes/no') # спрашиваем пользователя действительно ли он хочет удалить все товары
        answer =  input() # считываем подтверждение

        if answer == 'yes': # в случае подтверждения действительно удаляем все товары
            Product.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Succesfully wiped products!'))
            return

        self.stdout.write(self.style.ERROR('Access denied')) # в случае неправильного подтверждения, говорим что в доступе отказано

-------------Тайные функции админ-панели Django-------
Можно регистрировать модели в админке
simpleapp/admin.py

from django.contrib import admin
from .models import Category, Product

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)

# или разрегистрировать

admin.site.unregister(Product)
-------------
Зделать таблицу
admin.py

from django.contrib import admin
from .models import Category, Product

# создаём новый класс для представления товаров в админке
class ProductAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = [field.name for field in Product._meta.get_fields()] # генерируем список имён всех полей для более красивого отображения

# Register your models here.

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
-------------
Ограничить вывод полей
admin.py

from django.contrib import admin
from .models import Category, Product

# создаём новый класс для представления товаров в админке
class ProductAdmin(admin.ModelAdmin):
    # list_display - это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('name', 'price') # оставляем только имя и цену товара

# Register your models here.

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
---------------------------------------
К слову, поля не обязательно должны быть столбцами в БД. Например, в админке
вполне себе можно выводить какое-либо другое поле, например property. Давайте
допишем какое-нибудь свойство в нашу модель товаров:
models.py

class Product(models.Model):
    """
    Класс Product, отображает товары и имеет обязательные поля name,
    description, quantity,
    category, price.
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    quantity = models.IntegerField(
        validators=[MinValueValidator(0,
                                      'Quantity should be >= 0')])
    # Поле которое будет ссылаться на модель категории
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE,
                                 related_name='products')
    # все продукты в категории будут доступны через поле products
    price = models.FloatField(
        validators=[MinValueValidator(0.0,
                                      'Price should be >= 0')])

# допишем свойство, которое будет отображать есть ли товар на складе
    @property
    def on_stock(self):
        """
         Отображает есть ли товар на складе есть=True, нет=False
        """
        return self.quantity > 0

    def __str__(self):
        return (f'{self.category} : {self.name} : {self.quantity} :'
                f' {self.description[:20]}')
-------------
Допишем это же поле в fields в админке
admin.py

from django.contrib import admin
from .models import Category, Product

class ProductAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in Product._meta.get_fields()]
    list_display = ('name', 'price', 'quantity', 'on_stock')

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
# admin.site.unregister(Product)  # разрегистрируем наши товары
-------------
Для того, чтобы начать сортировать товары, например, по цене или по имени в
алфавитном порядке, и по любому свойству вообще, достаточно нажать по
заголовку в таблице. Это отсортирует товары по этому свойству.
-------------Фильтры в админке----
admin.py

class ProductAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in Product._meta.get_fields()]
    list_display = ('name', 'price', 'quantity', 'on_stock')

    list_filter = ('price', 'quantity', 'name')  # добавляем примитивные
    фильтры в нашу админку
-------------Группирует поо сатегории----
admin.py

class ProductAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in Product._meta.get_fields()]
    list_display = ('name', 'price', 'quantity', 'on_stock')
    list_filter = ('price', 'quantity', 'name')

    search_fields = ('name', 'category__name')  # тут всё очень похоже на
    фильтры из запросов в базу
-------------
В результате сверху у нас появилась строка, которая ищет на совпадения
параметры, которые вы укажите в поле search_fields. Так уже гораздо удобнее,
 можно искать как по категории, так и по названию товара
-------------Добавление действия "обнуление выделенных объектов"-----
admin.py

from django.contrib import admin
from .models import Category, Product

# напишем уже знакомую нам функцию обнуления товара на складе
def nullfy_quantity(modeladmin, request, queryset):  # все аргументы уже
        должны быть вам знакомы, самые нужные из них это request — объект
        хранящий информацию о запросе и queryset — грубо говоря набор
        объектов, которых мы выделили галочками.
    queryset.update(quantity=0)
    nullfy_quantity.short_description = 'Обнулить товары'  # описание для
        более понятного представления в админ панеле задаётся, как будто это объект


class ProductAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in Product._meta.get_fields()]
    list_display = ('name', 'price', 'quantity', 'on_stock')
    list_filter = ('price', 'quantity', 'name')
    search_fields = ('name', 'category__name')

    actions = [nullfy_quantity]  # добавляем действия в список


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
# admin.site.unregister(Product)  # разрегистрируем наши товары
-------------
нужное нам действие появилось в окошке action.
-------------
Похожим образом можно настроить и категории, и вообще любой другой объект.
При регистрации главное обязательно вторым аргументом указывать класс
модель-админа.
    Да и не забудьте, если вы вносите изменения в админ-панель в нескольких
приложениях, например, admin.py редактируется у вас в нескольких приложениях,
то в случае конфликта будут применяться те изменения, приложение которого
стоит ниже в списке INSTALLED_APPS в настройках.
---------------------------------------
D_12
==============================================================================
-------------

-------------

-------------

-------------

-------------

---------------------------------------

---------------------------------------



