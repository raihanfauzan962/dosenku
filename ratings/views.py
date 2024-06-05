from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from professors.models import Professor

from .models import Rating
from .forms import RatingForm

class AddRatingView(LoginRequiredMixin, CreateView):
    model = Rating
    form_class = RatingForm
    template_name = 'ratings/add_rating.html'

    def get_initial(self):
        professor = get_object_or_404(Professor, pk=self.kwargs['professor_id'])
        return {'professor': professor}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        professor = get_object_or_404(Professor, pk=self.kwargs['professor_id'])
        kwargs['professor'] = professor
        return kwargs

    def form_valid(self, form):
        professor = get_object_or_404(Professor, pk=self.kwargs['professor_id'])
        form.instance.professor = professor
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('professor_detail', kwargs={'pk': self.kwargs['professor_id']})

class EditRatingView(LoginRequiredMixin, UpdateView):
    model = Rating
    form_class = RatingForm
    template_name = 'ratings/edit_rating.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        rating = self.get_object()
        kwargs['professor'] = rating.professor
        return kwargs

    def form_valid(self, form):
        rating = self.get_object()
        form.instance.professor = rating.professor
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('professor_detail', kwargs={'pk': self.object.professor.pk})

class DeleteRatingView(DeleteView):
    model = Rating
    success_url = reverse_lazy('professor_list')
    template_name = 'ratings/delete_rating.html'

    def get_success_url(self):
        rating = self.get_object()
        professor = rating.professor
        return reverse_lazy('professor_detail', kwargs={'pk': professor.pk})

class AgreementView(TemplateView):
    template_name = 'ratings/agreement.html'

class GuidelinesView(TemplateView):
    template_name = 'ratings/guidelines.html'

@login_required
def like_review(request, rating_id):
    rating = get_object_or_404(Rating, pk=rating_id)
    if request.user in rating.dislikes.all():
        rating.dislikes.remove(request.user)

    if request.user in rating.likes.all():
        rating.likes.remove(request.user)
        messages.info(request, "You removed your like from this review.")
    else:
        rating.likes.add(request.user)
        messages.success(request, "You liked this review.")

    return redirect('professor_detail', pk=rating.professor.pk)

@login_required
def dislike_review(request, rating_id):
    rating = get_object_or_404(Rating, pk=rating_id)
    if request.user in rating.likes.all():
        rating.likes.remove(request.user)

    if request.user in rating.dislikes.all():
        rating.dislikes.remove(request.user)
        messages.info(request, "You removed your dislike from this review.")
    else:
        rating.dislikes.add(request.user)
        messages.success(request, "You disliked this review.")

    return redirect('professor_detail', pk=rating.professor.pk)
