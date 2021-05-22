from django.urls import path
from catalog.views import CategoryListView, AchievementListView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('achievements/', AchievementListView.as_view(), name='achievements'),
]
