from logging import disable

from django import forms
from django.core.exceptions import ValidationError
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory

from posts.mixins import ReadOnlyFieldsMixin
from posts.models import Post, Comment
from posts.validators import BadWordValidator

from crispy_forms.helper import FormHelper


class PostBaseForm(forms.ModelForm):
    content2 = forms.CharField(max_length=10,
        validators=[BadWordValidator(
            bad_words=['bad_word1', 'bad_word2'])],
    )

    class Meta:
        model = Post
        exclude = ('approved','author')

        widgets = {
            'language': forms.RadioSelect(
                attrs={'class': 'radio-select'},
            ),

        }

        help_texts = {
            'title': "This is a help text",
        }


    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title.lower() in content.lower():
            raise ValidationError("The post title shouldn`t be included in the content!")

        return cleaned_data

    def save(self, commit=True):
        post = super().save(commit=False)

        if commit:
            post.save()

        return post

class PostCreateForm(PostBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.for_id='id-exampleForm'
        self.helper.form_class = 'blueForms'

class PostEditForm(PostBaseForm):
    pass

class PostDeleteForm(ReadOnlyFieldsMixin, PostBaseForm):
    pass

class SearchForm(forms.Form):
    query = forms.CharField(label='', required=False, max_length=100,
                            widget=forms.TextInput(attrs={'placeholder': 'Search for posts...'}))

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '',

        }
        widgets = {
            'content': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Comment here...'}),
        }

CommentFormSet = formset_factory(CommentForm, extra=1)