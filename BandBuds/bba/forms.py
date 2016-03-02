from django import forms
from bba.models import Band

class BandForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the bands name.")
    city = forms.CharField(max_length=128, help_text="Please enter the city band is from.")
    country = forms.CharField(max_length=128, help_text="Please enter the country band is from.")
    formed = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    genre = forms.CharField(widget=forms.HiddenInput(), initial=" ")

    class Meta:
        model = Band
        fields = ('name',)
