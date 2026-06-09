from django.urls import path
from . import views

urlpatterns=[
    path('',views.home, name='home'),
    path('customer-list/',views.customer_list,name='customer_list'),
    path('add-book/',views.add_book,name='add_book'),
    path('view-books/', views.viewBooks, name='view_books'),
    path('signup/',views.signup, name='signup'),
    path('view-users/',views.viewUser),
    path('signin/',views.signin, name='signin'),
     path('signout/',views.signout, name='signout'),
     path('view_users/',views.view_users,name='view_users'),
]