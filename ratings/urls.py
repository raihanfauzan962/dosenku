from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:professor_id>/', views.AddRatingView.as_view(), name='add_rating'),
    path('edit/<int:pk>/', views.EditRatingView.as_view(), name='edit_rating'),
    path('delete/<int:pk>/', views.DeleteRatingView.as_view(), name='delete_rating'),
    
    path('like/<int:rating_id>/', views.like_review, name='like_review'),
    path('dislike/<int:rating_id>/', views.dislike_review, name='dislike_review'),
    
    path('agreement/', views.AgreementView.as_view(), name='agreement'),
    path('guidelines/', views.GuidelinesView.as_view(), name='guidelines'),
]
