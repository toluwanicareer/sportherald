from django import forms
from .models import Post
from .models import PostImage
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'body','tags','sport')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control borderprob' }),
            'body': forms.Textarea(attrs={'class': ' form-control'}),
            'tags': forms.Select(attrs={'class':'form-control'}),
        }

class ImageForm(forms.ModelForm) :
    class Meta:
        model = PostImage
        fields=('image',)

