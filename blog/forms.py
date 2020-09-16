from django import forms
from .models import Post

#PostForm이라는 form을 만들자
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)