from django import forms
from .models import Proposal


class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ['title', 'description']

        labels = {
            'title': 'Titel van uw voorstel',
            'description': 'Omschrijving',
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Geef uw voorstel een duidelijke titel...',
                'class': 'form-control',
                'maxlength': 200,
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Beschrijf uw voorstel zo duidelijk mogelijk...',
                'class': 'form-control',
                'rows': 6,
            }),
        }

