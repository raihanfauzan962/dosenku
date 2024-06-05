from django.views.generic import DetailView, ListView
from django.db import models
from django.db.models import Q, Avg

from .models import Professor
from ratings.models import Rating

import matplotlib.pyplot as plt
import base64
from io import BytesIO


class ProfessorListView(ListView):
    model = Professor
    template_name = "professors/professor_list.html"
    context_object_name = "professors"


class ProfessorDetailView(DetailView):
    model = Professor
    template_name = "professors/professor_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ratings = Rating.objects.filter(professor=self.object).order_by('-created_at')
        context["ratings"] = ratings

        # Calculate the average rating for Rate Your Dosen and Difficulty
        context['average_rate_your_dosen'] = (
            ratings.aggregate(Avg("rate_your_dosen"))["rate_your_dosen__avg"] or 0
        )
        context['average_difficulty'] = (
            ratings.aggregate(Avg("difficulty"))["difficulty__avg"] or 0
        )

        # Create a matplotlib figure for the average ratings
        fig, ax = plt.subplots(figsize=(6, 4))
        categories = ["Rating Dosen", "Kesulitan"]
        averages = [context['average_rate_your_dosen'], context['average_difficulty']]
        colors = [
            "green" if averages[0] > 3 else "red",  # Rating Dosen
            "red" if averages[1] > 3 else "green"   # Kesulitan
        ]

        # Bar chart
        ax.bar(categories, averages, color=colors)
        ax.set_ylim(0, 5)
        ax.set_ylabel("")
        ax.set_title("")

        # Save the plot to a BytesIO object in PNG format
        buf = BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png")
        plt.close(fig)

        # Encode the image in base64 and remove the bytes type
        context["chart"] = base64.b64encode(buf.getvalue()).decode("utf-8")
        return context



class ProfessorSearchView(ListView):
    model = Professor
    template_name = "professors/professor_search.html"
    context_object_name = "professors"

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        return Professor.objects.filter(
            models.Q(name__icontains=query)
            | models.Q(department__name__icontains=query)
            | models.Q(department__school__name__icontains=query)
            | models.Q(major__name__icontains=query)
            | models.Q(subjects__name__icontains=query)
        ).distinct()
