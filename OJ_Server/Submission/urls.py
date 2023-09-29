from django.urls import include, path
from . import views

urlpatterns = [
        path('verdict/<int:problem_id>', views.verdict, name='Verdict Page'),
]