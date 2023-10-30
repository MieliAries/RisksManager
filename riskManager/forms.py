from django import forms


class ProcessForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(max_length=200)


class RiskForm(forms.Form):
    name = forms.CharField(max_length=100)
    importance = forms.CharField(max_length=100)
    description = forms.CharField(max_length=100)
