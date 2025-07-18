from django.urls import path

from todos.views import TodoDetailView, TodoListCreateView
from todos.views import CategoriesView

urlpatterns = [
    path('', TodoListCreateView.as_view(), name='todo-list-create'),
    path('<int:pk>/', TodoDetailView.as_view(), name='todo_detail'),
    path('categories/', CategoriesView.as_view(), name='category-list'),


]