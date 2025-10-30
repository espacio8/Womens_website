from django.urls import path, re_path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.index, name='home'),  #http://coolsite.ru/
    path('about/', views.about, name='about'),
    path('cats/<int:cat_id>/', views.categories, name='cats_id'),  #http://coolsite.ru/cats/
    path('cats/<slug:cat_slug>/', views.categories_by_slug, name='cats'),  #http://coolsite.ru/cats/
    # re_path(r"^archive/(?P<year>[0-9]{4})/", views.archive)
    path("archive/<year4:year>/", views.archive, name='archive')
]