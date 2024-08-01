from django import forms


class pform(forms.Form):
    file = forms.FileField()

class episodForm(forms.Form):
    episod = forms.IntegerField(required=False,max_value=2000, min_value=1)


    