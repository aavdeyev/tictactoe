from django import forms

from models import pwdMgrModel

class pwdMgrModelForm(forms.ModelForm) :

    class Meta :
    
        model = pwdMgrModel

        fields = ('description', 'userName', 'passwd', 'comments')
