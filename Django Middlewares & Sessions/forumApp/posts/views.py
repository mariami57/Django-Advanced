from datetime import datetime

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models.query_utils import Q
from django.forms.models import modelform_factory
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls.base import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.base import View, TemplateView, RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView, FormMixin
from django.views.generic.list import ListView

from posts.decorators import measure_execution_time
from posts.forms import PostBaseForm, PostCreateForm, PostEditForm, PostDeleteForm, SearchForm, CommentForm, \
    CommentFormSet

from posts.models import Post


# Create your views here
# class IndexView(View):
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return super().dispatch(request, *args, **kwargs)
#         else:
#             return HttpResponse("403 Forbidden")
#
#     def get(self, request, *args, **kwargs):
#         return render(request, "index.html")


def counter_view(request):
    request.session['counter'] = request.session.get('counter', 0) + 1
    return HttpResponse(f"View count: {request.session['counter']}")

class IndexView(TemplateView):
    # template_name = 'index.html'
    # extra_context = {
    #     'current_time': datetime.now(),
    # }

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



# def dashboard(request):
    # search_form = SearchForm(request.GET)
    # posts = Post.objects.all()

    # if request.method == "GET" and search_form.is_valid():
    #     query = search_form.cleaned_data.get('query')
    #     posts = posts.filter(Q(title__icontains=query) |
    #                          Q(content__icontains=query) |
    #                          Q(author__icontains=query))

    # if request.method == "POST":
    #     return redirect('index')
    #
    # context = {
    #         "posts": posts,
    #         # "search_form": search_form,
    #     }
    #
    # return render(request, "posts/dashboard.html", context)

class CreatePost(LoginRequiredMixin, CreateView):
    form_class = PostCreateForm
    success_url = reverse_lazy('dashboard')
    model = Post
    template_name = 'posts/add_post.html'



# def add_post(request):
#     form = PostCreateForm(request.POST or None, request.FILES or None
#                           )
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return redirect('dashboard')
#
#     context = {"form": form}
#
#     return render(request, "posts/add_post.html", context)

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

# def edit_post(request, pk:int):
#     post = Post.objects.get(pk=pk)
#
#     if request.user.is_superuser:
#         PostEditForm = modelform_factory(Post, fields='__all__')
#     else:
#         PostEditForm = modelform_factory(Post, fields=('content',))
#
#     form = PostEditForm(request.POST or None, instance=post)
#
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return redirect('dashboard')
#
#     context = {"form": form}
#     return render(request, "posts/edit_post.html", context)

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

# def post_details(request, pk):
#
#     post = Post.objects.get(pk=pk)
    # comment_form_set = CommentFormSet(request.POST or None)
    #
    # if request.method == "POST" and comment_form_set.is_valid():
    #     for form in comment_form_set:
    #         comment = form.save(commit=False)
    #         comment.author = request.user.username
    #         comment.post = post
    #         comment.save()
    #         return redirect('details_post', pk=post.pk)

    #
    # context = {
    #     "post": post,
    #     # "formset": comment_form_set,
    # }
    #
    # return render(request, "posts/details_post.html", context)


class DeletePost(DeleteView, FormView):
    model = Post
    form_class = PostDeleteForm
    template_name = 'posts/delete_post.html'
    success_url = reverse_lazy('dashboard')


    def get_initial(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        post = self.model.objects.get(pk=pk)
        return post.__dict__

# def delete_post(request, pk):
#     post = Post.objects.get(pk=pk)
#     form = PostDeleteForm(instance=post)
#
#     if request.method == "POST":
#         post.delete()
#         return redirect('dashboard')
#
#     context = {
#         "form": form,
#     }
#
#     return render(request, "posts/delete_post.html", context)

class MyRedirectView(RedirectView):
    # url = 'http://localhost:8000/dashboard/'
    # pattern_name = 'dashboard'

    def get_redirect_url(self, *args, **kwargs):
        return reverse('dashboard') + "?query=Django"