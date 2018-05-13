from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    password2 = forms.CharField(widget=
        forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'password confirmation'
    }))
    class Meta:
        model= Post

        model = Post
        fields = ('title', 'password',)
        widgets = {
			'title':forms.TextInput(attrs={
				'class':'form-control forgot:active ',
				'placeholder':'Title'
				}),
            'password':forms.PasswordInput(attrs={
				'class':'form-control',
				'placeholder':'Password'
				}),
		}

    def clean(self):
        title = self.cleaned_data.get('title', None)
        password = self.cleaned_data.get('password', None)
        password2 = self.cleaned_data.get('password2', None)

        if title is None:
            raise forms.ValidationError("제목을 입력해주세요")
        if password is None:
            raise forms.ValidationError("패스워드를 입력해 주세요.")
        if password and password2 and password != password2:
            raise forms.ValidationError("두 비밀번호가 다릅니다.")
        return self.cleaned_data