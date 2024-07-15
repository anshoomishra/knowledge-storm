from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.forms import ModelForm
from django import forms
from blog.models import Article
from .models import Comment
from ckeditor.fields import RichTextFormField


class ArticleForm(ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Article
        fields = ['title','description','content']
        widgets = {
            "title":forms.TextInput(attrs={"class":"form-control","place-holder":"title"}),
            "description": forms.TextInput(attrs={"class": "form-control", "place-holder": "title"}),

        }
# forms.py

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'parent']
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control", "place-holder": "comment"}),


        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].required = False
        self.fields['parent'].widget = forms.HiddenInput()
