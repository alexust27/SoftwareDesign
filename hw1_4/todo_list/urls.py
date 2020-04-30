"""todo_list URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from todo_list import veiws

urlpatterns = [
    path('', veiws.index, name='index'),
    path('add/<l_id>', veiws.add_todo, name='add'),
    path('complete/<item_id>', veiws.complete_todo, name='complete'),
    path('create_tb', veiws.create_list, name='create_tb'),
    path('remove_list/<l_name>', veiws.remove_list, name='remove_list')
]
