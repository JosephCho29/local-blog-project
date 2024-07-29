from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('posts/', views.post_index, name='post-index'),
    path('posts/<int:post_id>/', views.post_detail, name='post-detail'),
    path('posts/create/', views.PostCreate.as_view(), name='post-create'),
    path('posts/<int:pk>/update/', views.PostUpdate.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name='post-delete'),
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('post/<int:post_id>/like/', views.like_post, name='like-post'),
    path('our-archive/', views.our_archive, name='our-archive'),
]
