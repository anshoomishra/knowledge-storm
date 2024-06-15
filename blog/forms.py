from ckeditor.widgets import CKEditorWidget
from django.forms import ModelForm
from django import forms
from blog.models import Article
from ckeditor.fields import RichTextFormField


class ArticleForm(ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Article
        fields = ['title','description','content']
        widgets = {
            "title":forms.TextInput(attrs={"class":"form-control","place-holder":"title"}),
            "description": forms.TextInput(attrs={"class": "form-control", "place-holder": "title"}),



        }
