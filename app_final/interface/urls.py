from django.urls import path
from interface.views import Interface, ABNChecker

urlpatterns = [
    path('api/abn_response', ABNChecker.as_view()),
    path('', Interface.as_view())
]
