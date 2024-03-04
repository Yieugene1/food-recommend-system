"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from food import views
from django.conf.urls.static import static
from django.conf import settings
from haystack.views import SearchView

urlpatterns = [
                  path('main/', views.index),
                  path('login/', views.login),
                  path('register/', views.register),
                  path('search/', views.search),
                  # path('search_result', views.search_result,name='search_result'),
                  path('logout/', views.logout),
                  path('main2/', views.main2),
                  path('main2/food1/', views.food1),
                  path('main2/food2/', views.food2),
                  path('main2/food3/', views.food3),
                  path('main2/food4/', views.food4),
                  path('updateinfo/', views.updateinfo),
                  path('chuan/', views.川菜),
                  path('hui/', views.徽菜),
                  path('zhe/', views.西安菜),
                  path('yue/', views.粤菜),
                  path('日本/', views.日本,name="日本"),
                  path('韩国/', views.韩国,name="韩国"),
                  path('法国/', views.法国,name="法国"),
                  path('意大利/', views.意大利,name="意大利"),
                  path('检索1/', views.检索1,name="检索1"),
                  path('浏览推荐/', views.浏览推荐,name="浏览推荐"),
                  path('个人喜好/', views.个人喜好,name="个人喜好"),
                  path('检索2/', SearchView(), name='haystack_search'),
                  path('su/', views.苏菜),
                  path('min/', views.闽菜),
                  path('xiang/', views.湘菜),
                  path('lu/', views.鲁菜),
                  path('detail_foods/<int:gid>', views.detail_foods, name='detail_foods'),
                  path('foods_save', views.foods_save, name='foods_save'),
                  path('user_save/', views.user_save, name='user_save'),
                  path('browse_user/', views.browse_user, name='browse_user'),
                  path('recommend_user/', views.recommend_user, name='recommend_user'),
                  path('recommend_all/', views.recommend_all, name='recommend_all'),
                  path('recommend', views.recommend, name='recommend'),
                  path('submit_rating', views.submit_rating, name='submit_rating'),
                  # path('search/', SearchView(), name='haystack_search'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
