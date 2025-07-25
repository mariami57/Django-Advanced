from django.conf.urls.static import static
from django.contrib.sitemaps.views import index
from django.urls.conf import path, include

from forumApp import settings
from posts import views
from posts.views import notify_all_users

urlpatterns = [
    path('', views.counter_view, name='index'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('add-post/', views.CreatePost.as_view(), name='add_post'),
    path('<int:pk>/',include([
        path('approve/', views.approve_post, name='approve_post'),
        path('edit-post', views.EditPost.as_view(), name='edit_post'),
        path('details-post', views.PostDetails.as_view(), name='details_post'),
        path('delete-post', views.DeletePost.as_view(), name='delete_post'),
    ]) ),

    path('redirect/', views.MyRedirectView.as_view(), name='redirect'),
    path('notify/', notify_all_users, name='notify'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)