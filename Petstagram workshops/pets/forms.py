from django import forms

from common.mixins import ReadOnlyMixin
from pets.models import Pet


class PetForm(forms.ModelForm):

    class Meta:
        model = Pet
        fields = ['name', 'date_of_birth', 'personal_photo']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Pet name'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'personal_photo': forms.TextInput(attrs={'placeholder': 'Link to image'}),
        }

        labels= {
            'name': 'Pet name',
            'date_of_birth': 'Date of birth',
            'personal_photo': 'Link ot image',
        }

class PetCreateForm(PetForm):
    pass

class PetEditForm(PetForm):
    pass

class PetDeleteForm(ReadOnlyMixin, PetForm):
    pass

