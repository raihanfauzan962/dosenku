from django.db import models
from django.contrib.auth import get_user_model
from professors.models import Professor, Subject

User = get_user_model()

class Rating(models.Model):
    RATE_YOUR_DOSEN_CHOICES = [
        (1, "Sangat buruk"),
        (2, "Buruk"),
        (3, "Biasa saja"),
        (4, "Bagus"),
        (5, "Sangat bagus")
    ]
    DIFFICULTY_CHOICES = [
        (1, "Sangat mudah"),
        (2, "Mudah"),
        (3, "Biasa saja"),
        (4, "Sulit"),
        (5, "Sangat sulit")
    ]

    RECOMMEND_CHOICES = [(True, 'Yes'), (False, 'No')]
    TEXTBOOK_SYLLABUS_CHOICES = [(True, 'Yes'), (False, 'No')]
    ATTENDANCE_CHOICES = [(True, 'Yes'), (False, 'No')]

    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rate_your_dosen = models.IntegerField(choices=RATE_YOUR_DOSEN_CHOICES, default=5)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=1)
    recommend = models.BooleanField(choices=RECOMMEND_CHOICES, default=True)
    uses_textbook = models.BooleanField(choices=TEXTBOOK_SYLLABUS_CHOICES, default=True)
    mandatory_attendance = models.BooleanField(choices=ATTENDANCE_CHOICES, default=True)
    review_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_reviews', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_reviews', blank=True)

    def likes_count(self):
        return self.likes.count()

    def dislikes_count(self):
        return self.dislikes.count()

    def __str__(self):
        if self.is_anonymous:
            return f"{self.professor.name} - {self.subject.name} - Anonymous"
        else:
            username = self.user.username if self.user else 'Anonymous'
            return f"{self.professor.name} - {self.subject.name} - {username}"
    
    is_anonymous = models.BooleanField(default=False, verbose_name="Anonymous review")

