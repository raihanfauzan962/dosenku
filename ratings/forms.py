from django import forms
from .models import Rating
from professors.models import Subject
from django.core.exceptions import ValidationError

RATE_CHOICES = [
    (1, '1 - Sangat buruk'),
    (2, '2 - Buruk'),
    (3, '3 - Biasa saja'),
    (4, '4 - Bagus'),
    (5, '5 - Sangat bagus')
]

DIFFICULTY_CHOICES = [
    (1, '1 - Sangat mudah'),
    (2, '2 - Mudah'),
    (3, '3 - Biasa saja'),
    (4, '4 - Sulit'),
    (5, '5 - Sangat sulit')
]

RECOMMEND_CHOICES = [(True, 'Ya'), (False, 'Tidak')]
TEXTBOOK_SYLLABUS_CHOICES = [(True, 'Ya'), (False, 'Tidak')]
ATTENDANCE_CHOICES = [(True, 'Ya'), (False, 'Tidak')]

class RatingForm(forms.ModelForm):
    agreement = forms.BooleanField(required=True, label="Saya setuju dengan ketentuan dan panduan")
    is_anonymous = forms.BooleanField(required=False, label="Tambah penilaian sebagai anonimous")

    class Meta:
        model = Rating
        fields = [
            'subject',
            'rate_your_dosen',
            'difficulty',
            'recommend',
            'uses_textbook',
            'mandatory_attendance',
            'review_text',
            'agreement',
            'is_anonymous'
        ]

    subject = forms.ModelChoiceField(queryset=Subject.objects.none(), widget=forms.Select(attrs={'class': 'form-select'}), label="Mata Kuliah")
    rate_your_dosen = forms.ChoiceField(choices=RATE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}), label="Rate dosen ini")
    difficulty = forms.ChoiceField(choices=DIFFICULTY_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}), label="Tingkat kesulitan dosen ini")
    recommend = forms.ChoiceField(choices=RECOMMEND_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}), label="Apa kamu ingin merekomendasikan dosen ini ke mahasiswa lain?")
    uses_textbook = forms.ChoiceField(choices=TEXTBOOK_SYLLABUS_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}), label="Apakah dosen ini mengikuti silabus dalam perkuliahan?")
    mandatory_attendance = forms.ChoiceField(choices=ATTENDANCE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}), label="Apakah kehadiran wajib pada dosen ini?")
    review_text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}), label="Berikan ulasan lengkap kamu terhadapa dosen ini")
    
    def __init__(self, *args, **kwargs):
        professor = kwargs.pop('professor', None)
        super().__init__(*args, **kwargs)
        if professor:
            self.fields['subject'].queryset = professor.subjects.all()
            self.fields['professor'] = forms.CharField(
                initial=professor.name,
                disabled=True,
                widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
            )
        self.fields['rate_your_dosen'].widget.attrs.update({'class': 'form-select'})
        self.fields['difficulty'].widget.attrs.update({'class': 'form-select'})
        self.fields['recommend'].widget.attrs.update({'class': 'form-select'})
        self.fields['uses_textbook'].widget.attrs.update({'class': 'form-select'})
        self.fields['mandatory_attendance'].widget.attrs.update({'class': 'form-select'})
        self.fields['review_text'].widget.attrs.update({'class': 'form-control', 'rows': 4})
        self.fields['agreement'].widget.attrs.update({'class': 'form-check-input'})

    def clean_agreement(self):
        if not self.cleaned_data.get('agreement'):
            raise ValidationError("You must agree to the terms and guidelines.")
        return self.cleaned_data['agreement']
