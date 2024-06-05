from allauth.account.forms import SignupForm
from django import forms
from django.core.validators import RegexValidator

class CustomSignupForm(SignupForm):
    npm = forms.CharField(
        max_length=8,
        validators=[RegexValidator(r'^\d{8}$')],
        label='NPM',
        required=True,
        help_text="Masukkan 8 digit NPM anda. NPM digunakan untuk verifikasi bahwa anda adalah mahasiswa Universitas Gunadarma.",
        widget=forms.TextInput(attrs={
            'placeholder': 'NPM',
        })
    )

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.npm = self.cleaned_data['npm']
        user.save()
        return user
