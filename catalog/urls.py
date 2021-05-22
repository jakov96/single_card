from django.urls import path
from catalog.views import CategoryListView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
]
