from django import forms


class HelloForm(forms.Form):
    name = forms.CharField(min_length=3, max_length=1000, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'autocomplete': 'off', 'pattern': '[A-Za-z ]+', 'title': 'Enter Characters Only '}))
    surname = forms.CharField(min_length=3, max_length=1000, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'autocomplete': 'off', 'pattern': '[A-Za-z ]+', 'title': 'Enter Characters Only '}))
    age = forms.IntegerField(min_value=0, max_value=110, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'autocomplete': 'off', 'pattern': '[0-9 ]+', 'title': 'Enter Numbers Only '}))
