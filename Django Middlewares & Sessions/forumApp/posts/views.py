import asyncio
from datetime import datetime

from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models.query_utils import Q
from django.forms.models import modelform_factory
from django.http.response import HttpResponse
from django.shortcuts import  redirect
from django.urls.base import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView, FormMixin
from django.views.generic.list import ListView

from posts.decorators import measure_execution_time
from posts.forms import  PostCreateForm, PostEditForm, PostDeleteForm, SearchForm, \
    CommentFormSet

from posts.models import Post
from posts.tasks import _send_mail

UserModel = get_user_model()


def counter_view(request):
    request.session['counter'] = request.session.get('counter', 0) + 1
    return HttpResponse(f"View count: {request.session['counter']}")

class IndexView(TemplateView):
    def get_context_data(self, **kwargs):
        super().get_context_data(**kwargs)
        kwargs.update({
            "current_time":datetime.now(),
        })
        return kwargs


    def get_template_names(self):
        if self.request.user.is_superuser:
            return ['index_for_admin.html']
        return ['index.html']


def approve_post(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        post.approved = True
        post.save()

        return redirect('dashboard')

@method_decorator(name='dispatch', decorator=measure_execution_time)
class Dashboard(ListView, PermissionRequiredMixin):
    model = Post
    template_name = "posts/dashboard.html"
    paginate_by = 4
    query_param = "query"
    form_class = SearchForm
    permission_required = "posts.approve_post"

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs.update({
            "search_form": self.form_class(),
            "query": self.request.GET.get(self.query_param, ''),
        })
        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self):
        queryset = self.model.objects.all()
        search_value = self.request.GET.get(self.query_param)

        if not self.has_permission():
            queryset = queryset.filter(approved=True)

        if self.query_param in self.request.GET:
            queryset = queryset.filter(Q(title__icontains=search_value) |
                             Q(content__icontains=search_value) |
                             Q(author__icontains=search_value))
        return queryset


class CreatePost(LoginRequiredMixin, CreateView):
    form_class = PostCreateForm
    success_url = reverse_lazy('dashboard')
    model = Post
    template_name = 'posts/add_post.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class EditPost(UpdateView):
    model = Post
    success_url = reverse_lazy('dashboard')
    template_name = 'posts/edit_post.html'
    form_class = PostEditForm

    def get_form_class(self):
        if self.request.user.is_superuser:
            return modelform_factory(Post, fields='__all__')
        else:
            return modelform_factory(Post, fields=('content',),)


class PostDetails(DetailView, FormMixin):
    model = Post
    template_name = 'posts/details_post.html'
    form_class = CommentFormSet

    def get_context_data(self, **kwargs):
        kwargs.update({
            "formset":self.get_form_class()()
        })

        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse_lazy('details_post', kwargs={'pk':self.kwargs.get(self.pk_url_kwarg)})

    def get_form_class(self):
        return CommentFormSet

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form_set = self.get_form_class()(request.POST or None)

        if comment_form_set.is_valid():
            for form in comment_form_set:
                comment = form.save(commit=False)
                comment.author = request.user.username
                comment.post = self.object
                comment.save()

            return self.form_valid(comment_form_set)


class DeletePost(DeleteView, FormView):
    model = Post
    form_class = PostDeleteForm
    template_name = 'posts/delete_post.html'
    success_url = reverse_lazy('dashboard')


    def get_initial(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        post = self.model.objects.get(pk=pk)
        return post.__dict__


class MyRedirectView(RedirectView):
    # url = 'http://localhost:8000/dashboard/'
    # pattern_name = 'dashboard'

    def get_redirect_url(self, *args, **kwargs):
        return reverse('dashboard') + "?query=Django"



async def send_mail(*args):
    await _send_mail(*args)

async def notify_all_users(request):
    all_users = await sync_to_async(UserModel.objects.all)()
    users = await sync_to_async(list)(all_users)

    email_tasks = [
       send_mail(
           'Maintenance',
           'We are having a maintenance! We will be back shortly!',
           settings.DEFAULT_FROM_EMAIL,
           [user.email]

       ) for user in users
    ]

    await asyncio.gather(*email_tasks)