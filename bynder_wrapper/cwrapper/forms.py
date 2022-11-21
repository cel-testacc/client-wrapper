from django import forms

class UploadFileForm(forms.Form):
    token = forms.CharField(label='Access Bearer Token', max_length=50)
    file = forms.FileField()
