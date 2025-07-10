from django.shortcuts import render, redirect, resolve_url
from django.views.generic import ListView
from pyperclip import copy

from common.forms import CommentForm, SearchForm
from pets.models import Pet
from photos.models import Photo
from common.models import Like


# Create your views here.
class HomePageView(ListView):
    template_name = 'common/home-page.html'
    model = Photo
    context_object_name = 'all_photos'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs.update({
            'comment_form': CommentForm(),
            'search_form': SearchForm(),
        })
        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        pet_name = self.request.GET.get('text')

        if pet_name:
            queryset = queryset.prefetch_related('tagged_pets', 'like_set').filter(
                tagged_pets__name__icontains=pet_name
            )

        return queryset


def like_functionality(request, photo_id:int):
    liked_photo = Like.objects.filter(to_photo_id=photo_id).first()

    if liked_photo:
        liked_photo.delete()
    else:
        Like.objects.create(
            to_photo_id=photo_id,
        )
    return redirect(request.META.get('HTTP_REFERER') + f'#{photo_id}')

def share(request, photo_id:int):
    copy(request.META.get('HTTP_HOST') + resolve_url('details_photo', photo_id))

    return redirect(request.META.get('HTTP_REFERER') + f'#{photo_id}')

def add_comment(request, photo_id:int):
    form = CommentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.to_photo = Photo.objects.get(pk=photo_id)
        comment.save()

    return redirect(request.META.get('HTTP_REFERER') + f'#{photo_id}')