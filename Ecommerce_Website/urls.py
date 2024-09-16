from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),

    # Homme Ecommerce Website
    path('base/', views.materiel_HOME, name='base'),

    path('materiel/', views.materiel_home, name='materiel'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:foo>', views.category, name='category'),
    path('category_summary/', views.category_summary, name='category_summary'),

    # Search
    path('search/', views.search, name='search'),


    # Account
    path('login/', views.login_user,name='login'),
    path('logout/', views.logout_user,name='logout'),
    path('register/', views.register_user,name='register'),
    path('update_user/', views.update_user,name='update_user'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_info/', views.update_info,name='update_info'),

]
