from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model, authenticate
from .models import User
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm

class PasswordChangeForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.user = user
        super().__init__(*args, **kwargs)

    old_password = forms.CharField(widget=
        forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'old_password'
    }))

    new_password = forms.CharField(widget=
        forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'new_password'
    }))

    confirm_password = forms.CharField(widget=
        forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'new_password2'
    }))

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError("현재 비밀번호가 틀렸습니다.")
        return old_password
    
    #두 비밀번호 검증시 필드 순서에 따라 동일한 타입의 필드가 존재한다면
    #하나의 필드에 종속되기 때문에 부모 타입의 필드로 clean_filedname하면
    #종속된 필드들은 cleaned_data목록에 존재하지 않는다. 따라서 종속된
    #필드의 값을 사용하려면 종속된 데이터 필드명으로 clean작업을 수행해야한다.
    def clean_confirm_password(self): 
        password1 = self.cleaned_data.get('new_password')
        password2 = self.cleaned_data.get('confirm_password')
        if password1 != password2:
            raise forms.ValidationError("두 비밀번호가 다릅니다.")
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password'])
        if commit:
            self.user.save()
        return self.user
            
class LoginForm(forms.Form):
    email = forms.CharField(widget=
    forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Email',
    }))
    password = forms.CharField(widget=
        forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'password'
    }))

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('email', None)
        password = self.cleaned_data.get('password', None)

        if username is None:
            raise forms.ValidationError("email을 입력해주세요")
        if password is None:
            raise forms.ValidationError("패스워드를 입력해 주세요.")
        if username and password:
            self.user_cache = authenticate(username = username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("email 또는 pwd를 확인해 주세요")
        return self.cleaned_data
    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.
        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.
        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                "에러"
            )
    
    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache



class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password',})
    )
    password2 = forms.CharField(
        label='Password confirmation', 
        widget=forms.PasswordInput(attrs={'class':'form-control' , 'placeholder':'Password Confirmation',})
    )

    class Meta:
        model = get_user_model()
        fields = ['email']
        widgets = {
			'email':forms.EmailInput(attrs={
				'class':'form-control',
				'placeholder':'Email'
				}),
		}

    
    def clean(self):
        email = self.cleaned_data.get("email",None)
        password1 = self.cleaned_data.get("password1",None)
        password2 = self.cleaned_data.get("password2",None)
        password1_isalpha = password1[0].isalpha()

        if len(password1) < 8:
            raise forms.ValidationError("비밀번호가 짧습니다. 최소 8글자 이상 입력해 주세요(영문+숫자)")
        if all(c.isalpha() == password1_isalpha for c in password1):
            raise forms.ValidationError("비밀번호는 영문과 숫자 조합으로 다시 입력해 주세요.")
        if password1 and password2 and password1 != password2:
            print("들어와?")
            raise forms.ValidationError("두 비밀번호가 다릅니다.")
        if email is None:
            raise forms.ValidationError("이메일을 입력해주세요.")
        else:
            user_data=User.objects.all()
            user_data= user_data.filter(email=email)
            if user_data:
                raise forms.ValidationError("동일한 이메일이 존재합니다.")
        return self.cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

#admin전용 변경
class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'is_active', 'is_staff']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]