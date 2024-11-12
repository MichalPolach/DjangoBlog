from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:year>/', views.post_list, name='post_list_year'),
    path('<int:year>/<int:month>/', views.post_list, name='post_list_month'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),  # Changed from pk to slug
    path('post/new/', views.post_new, name='post_new'),
    path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),  # Changed from pk to slug
]