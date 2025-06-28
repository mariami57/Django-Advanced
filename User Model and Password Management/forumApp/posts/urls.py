from django.conf.urls.static import static
from django.contrib.sitemaps.views import index
from django.urls.conf import path

from forumApp import settings
from posts import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('add-post/', views.CreatePost.as_view(), name='add_post'),
    path('approve/<int:pk>/', views.approve_post, name='approve_post'),
    path('edit-post/<int:pk>/', views.EditPost.as_view(), name='edit_post'),
    path('details-post/<int:pk>/', views.PostDetails.as_view(), name='details_post'),
    path('delete-post/<int:pk>/', views.DeletePost.as_view(), name='delete_post'),
    path('redirect/', views.MyRedirectView.as_view(), name='redirect'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)