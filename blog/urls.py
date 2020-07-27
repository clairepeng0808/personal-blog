from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.PostListView.as_view(),name='post_list'),
    # path('about/', views.AboutView.as_view(),name='about'),
    path('post/<int:pk>/', views.PostDetailView.as_view(),name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(),name='new'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(),name='edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(),name='post_remove'),
    path('drafts/',views.DraftListView.as_view(),name='draft_list'),
    path('drafts/<int:pk>/publish',views.publish_draft,name='publish_draft'),
    path('post/<int:pk>/comment/',views.add_comment_to_post,name='add_comment'),
    path('comment/<int:pk>/approve',views.approve_comment,name='approve_comment'),
    path('comment/<int:pk>/remove',views.remove_comment,name='remove_comment'),
]