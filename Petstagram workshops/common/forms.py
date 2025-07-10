from django import forms

from common.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']

        widgets = {
            'comment_text': forms.Textarea(attrs={
                'placeholder': 'Add a comment...',
                'cols':40,
                'rows':10,

            }),
        }


class SearchForm(forms.Form):
    text = forms.CharField(max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by pet name...',}))