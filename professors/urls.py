from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProfessorListView.as_view(), name='professor_list'),
    path('<int:pk>/', views.ProfessorDetailView.as_view(), name='professor_detail'),
    path('search/', views.ProfessorSearchView.as_view(), name='professor_search'),
]
