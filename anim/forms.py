from django import forms
from . import models

class pform(forms.ModelForm):
    class Meta:
        model = models.anim_video
        fields = ['video']


class animForme(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name_english'].widget.attrs['class'] = 'form-control'
        self.fields['name_english'].label = 'نام انگلیسی'
        self.fields['name_farsi'].widget.attrs['class'] = 'form-control'
        self.fields['name_farsi'].label = 'نام فارسی'
        self.fields['name_Japanese'].widget.attrs['class'] = 'form-control'
        self.fields['name_Japanese'].label = 'نام ژاپنی'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].label = 'توضیحات'
        self.fields['status'].widget.attrs['class'] = 'form-control'
        self.fields['status'].label = 'وضعیت'
        self.fields['seasion'].widget.attrs['class'] = 'form-control'
        self.fields['seasion'].label = 'فصل'
        self.fields['max_episod'].widget.attrs['class'] = 'form-control'
        self.fields['max_episod'].label = 'حداکثر قسمت'
        self.fields['photo'].widget.attrs['class'] = 'form-control'
        self.fields['photo'].label = 'تصویر'
        self.fields['tags'].widget.attrs['class'] = 'form-control'
        self.fields['tags'].widget.attrs['data-role'] = "tagsinput"
        self.fields['tags'].label = 'تگ ها'
        
    class Meta:
        model = models.anim
        fields = ['photo','name_english','name_farsi','name_Japanese','description','status','seasion','max_episod','tags']
    

        

class animForm(forms.Form):
    status = (
        ('منتشر نشده','منتشر نشده'),
        ('در حال انتشار','در حال انتشار'),
        ('منتشر شده','منتشر شده'),
    )
    photo = forms.ImageField()
    name_english = forms.CharField(max_length=255)
    name_farsi = forms.CharField(max_length=255)
    name_Japanese = forms.CharField(max_length=255)
    description = forms.CharField()
    status = forms.ChoiceField(choices=status)
    seasion = forms.IntegerField(min_value=1,max_value=10)
    max_episod = forms.IntegerField(min_value=1)
